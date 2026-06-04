import unittest
from unittest.mock import MagicMock
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import TableNotFoundError
from src.db.backend.table import Table


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = MemoryDatabase()

    def test_table_exists(self) -> None:
        self.assertFalse(self.db._table_exists("students"))
        mock_table = MagicMock(spec=Table)
        self.db._save_table("students", mock_table)
        self.assertTrue(self.db._table_exists("students"))

    def test_load_table_success(self) -> None:
        mock_table = MagicMock(spec=Table)
        self.db._save_table("students", mock_table)
        self.assertEqual(self.db._load_table("students"), mock_table)

    def test_load_table_not_found(self) -> None:
        with self.assertRaises(TableNotFoundError):
            self.db._load_table("absent_table")


if __name__ == "__main__":
    unittest.main()
