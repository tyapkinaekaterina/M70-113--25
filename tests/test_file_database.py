import tempfile
import unittest
import json
from pathlib import Path

from src.db.backend.errors import (
    TableNotFoundError, 
    TableAlreadyExistsError, 
    MissingColumnError, 
    UnknownColumnError, 
    InvalidStorageDataError
)
from src.db.backend.file import FileDatabase

class TestFileDatabase(unittest.TestCase):
    def test_data_is_saved_between_instances(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)
            first_db.create_table("students", ("student_id", "name"))
            first_db.insert_record("students", {"student_id": 1, "name": "Иван"})

            second_db = FileDatabase(directory)
            records = second_db.select_records("students")
            self.assertEqual(records, [{"student_id": 1, "name": "Иван"}])

    def test_select_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("student_id", "name"))
            db.insert_record("students", {"student_id": 1, "name": "Иван"})
            db.insert_record("students", {"student_id": 2, "name": "Мария"})

            records = db.select_records("students", name="Мария")
            self.assertEqual(records, [{"student_id": 2, "name": "Мария"}])

    def test_select_from_missing_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            with self.assertRaises(TableNotFoundError):
                db.select_records("students")

    def test_create_already_exists_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(TableAlreadyExistsError):
                db.create_table("students", ("id", "name"))

    def test_missing_column_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(MissingColumnError):
                db.insert_record("students", {"id": 1})

    def test_unknown_column_error_on_insert(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(UnknownColumnError):
                db.insert_record("students", {"id": 1, "name": "Х", "age": 20})

    def test_unknown_column_error_on_select(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            with self.assertRaises(UnknownColumnError):
                db.select_records("students", unknown_field="test")

    def test_invalid_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            
            file_path = Path(directory) / "students.json"
            with file_path.open("w", encoding="utf-8") as f:
                f.write("Сломанный НЕ-JSON текст")
                
            with self.assertRaises(InvalidStorageDataError):
                db.select_records("students")

    def test_invalid_structure_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("id", "name"))
            
            file_path = Path(directory) / "students.json"
            with file_path.open("w", encoding="utf-8") as f:
                json.dump({"bad_key": 123}, f)
                
            with self.assertRaises(InvalidStorageDataError):
                db.select_records("students")

if __name__ == "__main__":
    unittest.main()
    def test_update_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("student_id", "name"))
            db.insert_record("students", {"student_id": 1, "name": "Иван"})
            
            # Обновляем имя для студента с id=1
            db.update_records("students", {"name": "Пётр"}, student_id=1)
            
            records = db.select_records("students")
            self.assertEqual(records, [{"student_id": 1, "name": "Пётр"}])

    def test_delete_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("student_id", "name"))
            db.insert_record("students", {"student_id": 1, "name": "Иван"})
            
            # Удаляем запись
            db.delete_records("students", student_id=1)
            
            records = db.select_records("students")
            self.assertEqual(records, [])
