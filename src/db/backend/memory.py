
from .errors import DuplicateIDError, InvalidAgeError

type StudentRecord = tuple[int, str, str, int, str]

class StudentTable:
    def __init__(self) -> None:
        self._student: list[StudentRecord] = []

    def create_record(self, student_id, first_name, second_name, age, sex):
        if age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")
        if any(rec[0] == student_id for rec in self._student):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        new_record = (student_id, first_name.strip(), second_name.strip(), age, sex.strip())
        self._student.append(new_record)
        return new_record

    def select_record(self, student_id=None, first_name=None, second_name=None, age=None, sex=None):
        if all(v is None for v in [student_id, first_name, second_name, age, sex]):
            return self._student.copy()
        
        result = []
        for record in self._student:
            if student_id is not None and record[0] != student_id: continue
            if first_name is not None and record[1] != first_name: continue
            if second_name is not None and record[2] != second_name: continue
            if age is not None and record[3] != age: continue
            if sex is not None and record[4] != sex: continue
            result.append(record)
        return result
