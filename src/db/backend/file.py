# src/db/backend/file.py
import json
from pathlib import Path

from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table


class FileDatabase(Database):
    """База данных, которая хранит таблицы в JSON-файлах."""

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        table_path = self._get_table_path(table_name)
        if not table_path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")

        try:
            with table_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise InvalidStorageDataError(
                "Файл таблицы содержит некорректный JSON."
            ) from error

        return self._deserialize_table(data)

    def _save_table(self, table_name: str, table: Table) -> None:
        table_path = self._get_table_path(table_name)

        with table_path.open("w", encoding="utf-8") as file:
            json.dump(
                self._serialize_table(table),
                file,
                ensure_ascii=False,
                indent=2,
            )

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _serialize_table(self, table: Table) -> dict:
        return {
            "columns": list(table.columns),
            "records": [record.copy() for record in table.records],
        }

    def _deserialize_table(self, data: dict) -> Table:
        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError("Файл таблицы имеет некорректную структуру.")

        columns = tuple(data["columns"])
        records = data.get("records", [])
        return Table(columns, records)

    def update_records(self, table_name: str, data: dict, **filters) -> None:
        """Обновляет записи в таблице, соответствующие фильтрам."""
        table = self._load_table(table_name)

        # Загружаем текущие данные из файла JSON
        records = self._deserialize_table(table_name)

        # Валидируем передаваемые для обновления поля через класс Table
        for column in data.keys():
            if column not in table.columns:
                from src.db.backend.errors import UnknownColumnError

                raise UnknownColumnError(f"Колонка {column} не существует")

        updated_count = 0
        for record in records:
            # Проверяем, подходит ли запись под фильтры
            if all(record.get(k) == v for k, v in filters.items()):
                record.update(data)
                updated_count += 1

        # Сохраняем обновленный массив обратно в файл
        self._serialize_table(table_name, records)

    def delete_records(self, table_name: str, **filters) -> None:
        """Удаляет записи из таблицы, соответствующие фильтрам."""
        self._load_table(table_name)  # Проверяем, существует ли таблица

        records = self._deserialize_table(table_name)

        # Оставляем только те записи, которые НЕ подходят под фильтры
        filtered_records = [
            record
            for record in records
            if not all(record.get(k) == v for k, v in filters.items())
        ]

        # Перезаписываем файл JSON
        self._serialize_table(table_name, filtered_records)
