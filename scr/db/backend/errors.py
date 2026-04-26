class StudentTableError(Exception):
    """Базовый класс для всех ошибок таблицы"""
    pass

class InvalidAgeError(StudentTableError):
    """Ошибка: возраст не может быть меньше 0"""
    pass

class DuplicateIDError(StudentTableError):
    """Ошибка: такой ID уже занят"""
    pass
