import unittest
from src.db.backend.memory import StudentTable
from src.db.backend.errors import InvalidAgeError, DuplicateIDError

class TestMemory(unittest.TestCase):

    def setUp(self):
        # Создаем экземпляр таблицы перед каждым тестом
        self.student_table = StudentTable()
        self.assertIsInstance(self.student_table, StudentTable)

    def test_create_record(self):
        # Набор тестовых данных для проверки создания записей
        cases = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
            (4, "Bob", "Brown", 21, "M"),
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.student_table.create_record(*test_data)
                self.assertEqual(record, test_data)

    def test_create_record_negative_age(self):
        # Проверка выброса исключения при отрицательном возрасте
        cases = [
            (1, "John", "Doe", -1, "M"),
            (2, "Jane", "Smith", -5, "F"),
        ]
        error_message = "Поле age не может быть отрицательным."

        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidAgeError) as context:
                    self.student_table.create_record(*test_data)
                self.assertEqual(str(context.exception), error_message)

    def test_create_record_duplicate_id(self):
        # Проверка выброса исключения при дублировании ID
        test_data_1 = (1, "John", "Doe", 20, "M")
        test_data_2 = (1, "Jane", "Smith", 22, "F")
        error_message = "Запись с id=1 уже существует."

        self.student_table.create_record(*test_data_1)

        with self.assertRaises(DuplicateIDError) as context:
            self.student_table.create_record(*test_data_2)
        self.assertEqual(str(context.exception), error_message)

    def test_select_record(self):
        # Проверка фильтрации и поиска записей
        test_datas = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
        ]

        for data in test_datas:
            self.student_table.create_record(*data)

        # Тестирование различных фильтров
        cases = [
            {
                "name": "Выбор без фильтров",
                "filters": {},
                "expected": test_datas,
            },
            {
                "name": "Фильтр по ID",
                "filters": {"student_id": 1},
                "expected": [test_datas[0]],
            },
            {
                "name": "Фильтр по имени",
                "filters": {"first_name": "Jane"},
                "expected": [test_datas[1]],
            },
        ]

        for case in cases:
            with self.subTest(case=case["name"]):
                records = self.student_table.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])
def test_select_record(self):
        # Сначала наполняем таблицу данными
        test_datas = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
        ]
        for data in test_datas:
            self.student_table.create_record(*data)

        # Проверяем разные варианты поиска
        cases = [
            {
                "name": "Выбор без фильтров (все)",
                "filters": {},
                "expected": test_datas,
            },
            {
                "name": "Фильтр по ID",
                "filters": {"student_id": 1},
                "expected": [test_datas[0]],
            },
            {
                "name": "Фильтр по полу",
                "filters": {"sex": "F"},
                "expected": [test_datas[1], test_datas[2]],
            },
        ]

        for case in cases:
            with self.subTest(case=case["name"]):
                records = self.student_table.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])