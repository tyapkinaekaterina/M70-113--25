import unittest
from unittest.mock import patch
from src.db.tui import main_menu

class TestTUI(unittest.TestCase):

    def test_full_coverage(self):
        # Этот список полностью покрывает все ветки if/elif/else и блоки ошибок
        inputs = [
            "1",        # Выбор: Добавить
            "1",        # ID
            "Ivan",     # Имя
            "Ivanov",   # Фамилия
            "20",       # Возраст
            "M",        # Пол
            "1",        # Выбор: Добавить снова (проверить ошибку дубликата ID)
            "1",        # Тот же ID
            "Masha",    # Имя
            "Sidorova", # Фамилия
            "22",       # Возраст
            "W",        # Пол
            "1",        # Выбор: Добавить (проверить ошибку некорректного возраста)
            "2",        # ID
            "Petya",    # Имя
            "Petrov",   # Фамилия
            "-5",       # Отрицательный возраст -> вызовет InvalidAgeError
            "M",        # Пол
            "1",        # Выбор: Добавить (проверить ValueError на буквах вместо цифр)
            "invalid",  # Буквы вместо ID -> вызовет ValueError
            "2",        # Выбор: Показать базу в консоли
            "3",        # Выбор: Обновить
            "1",        # ID для обновления
            "Petr",     # Новое имя
            "Petrov",   # Новая фамилия
            "21",       # Новой возраст
            "M",        # Новый пол
            "4",        # Выбор: Удалить
            "1",        # ID для удаления
            "999",      # Неверный пункт меню (уйдет в else/новую итерацию)
            "0",        # Выбор: Выход
        ]

        # Железно перехватываем input и print через контекстный менеджер
        with patch("builtins.input", side_effect=inputs) as mock_input, \
             patch("builtins.print") as mock_print:
            
            main_menu()

            # Проверяем финальный аккорд
            mock_print.assert_any_call("До свидания!")

if __name__ == "__main__":
    unittest.main()
