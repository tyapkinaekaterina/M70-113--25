import sys
import pytest
from unittest.mock import patch

def test_main_execution():
    """Тестируем точку входа __main__.py"""
    # Изолируем sys.argv
    with patch.object(sys, 'argv', ['__main__.py']):
        # Перехватываем run из tui, чтобы он ничего не запускал
        with patch('src.db.tui.run') as mock_run:
            
            # Удаляем модуль из кэша, если он там был, чтобы код выполнился заново
            if 'src.db.__main__' in sys.modules:
                del sys.modules['src.db.__main__']
                
            # Подменяем имя окружения на '__main__' перед импортом
            with patch('src.db.__main__.__name__', '__main__'):
                import src.db.__main__
            
            # Проверяем, зашел ли Python в блок if __name__ == "__main__":
            mock_run.assert_called_once()
