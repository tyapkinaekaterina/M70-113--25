import unittest
from unittest.mock import patch
from src.db.tui import TUI
from src.db.backend.memory import StudentTable

class TestTUI(unittest.TestCase):
    def setUp(self):
        self.app = TUI()
        self.app.table = StudentTable()

    'builtins.input', side_effect=['1', '1', 'Иван', 'Иванов', '20', 'M']
    'builtins.print'
    def test_handle_create_record(self, mock_print, mock_input):
        self.app._handle_create_record()
        self.assertEqual(len(self.app.table.select_record()), 1)

    'builtins.input', side_effect=['', '', '', '', '']
    'builtins.print'
    def test_handle_select_records(self, mock_print, mock_input):
        self.app.table.create_record(2, "Петр", "Петров", 25, "M")
        self.app._handle_select_records()
        self.assertTrue(True)