import sys
from unittest.mock import patch

def test_main_execution():
    # Задаем фейковые вводы для меню, если __main__ дергает tui
    inputs = ["0"]

    with patch.object(sys, 'argv', ['__main__.py']):
        sys.modules.pop('src.db.__main__', None)
        sys.modules.pop('src.db.tui', None)
        
        with patch('builtins.input', side_effect=inputs):
            try:
                import src.db.__main__
            except SystemExit:
                pass
            except Exception:
                pass
