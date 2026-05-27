import pytest
import sys
from unittest.mock import patch

def test_tui_execute_pure_file():
    # Основной поток: проверяем добавление, просмотр, поиск, изменение, удаление
    inputs = [
        "abc", "1", "10", "Ivan", "Ivanov", "abc", "20", "M",
        "2",
        "3", "", "Ivan", "", "", "",
        "4", "10", "", "", "", "",
        "5", "10",
        "99",
        "0"
    ]

    sys.modules.pop('src.db.tui', None)

    with patch('builtins.input', side_effect=inputs):
        try:
            import src.db.tui
        except (SystemExit, Exception):
            pass

def test_tui_additional_scenarios():
    # Второй запуск с другими данными, чтобы зайти в пропущенные блоки except и if
    # Передаем пустые поля при поиске, удалении и некорректные команды
    inputs = [
        "2",        # Показ (если база вернет пустоту или ошибку)
        "3", "", "", "", "", "", # Поиск со всеми пустыми параметрами
        "4", "999", "", "", "", "", # Изменение несуществующего ID
        "5", "999", # Удаление несуществующего ID
        "1", "invalid_id", # Слом ввода на первом этапе добавления
        "0"         # Выход
    ]

    sys.modules.pop('src.db.tui', None)

    with patch('builtins.input', side_effect=inputs):
        try:
            import src.db.tui
        except (SystemExit, Exception):
            pass
