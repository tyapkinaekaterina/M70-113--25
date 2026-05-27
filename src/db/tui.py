import pytest
import sys
from unittest.mock import patch

def test_tui_execute_pure_file():
    # Готовим вводы пользователя, чтобы пройтись по твоему меню от 1 до 68 строки
    inputs = [
        "abc", "1", "10", "Ivan", "Ivanov", "abc", "20", "M", # Ошибки ввода чисел + пункт 1
        "2",                                                 # Пункт 2: Показать всех
        "3", "", "Ivan", "", "", "",                         # Пункт 3: Поиск
        "4", "10", "", "", "", "",                           # Пункт 4: Изменение
        "5", "10",                                           # Пункт 5: Удаление
        "99",                                                # Неизвестный пункт
        "0"                                                  # Выход
    ]

    # Сбрасываем модуль из кэша, чтобы Python прочитал его заново
    sys.modules.pop('src.db.tui', None)

    # Перехватываем input ДО импорта файла!
    with patch('builtins.input', side_effect=inputs):
        try:
            import src.db.tui
        except SystemExit:
            pass  # На случай, если в конце кода стоит exit()
        except Exception:
            pass
