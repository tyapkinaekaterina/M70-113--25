from .errors import DuplicateIDError, InvalidAgeError

type StudentRecord = tuple[int, str, str, int, str]


class StudentTable:
    def __init__(self) -> None:
        self._student: list[StudentRecord] = []

    def create_record(
        self,
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
    ) -> StudentRecord:

        if age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        if any(record[0] == student_id for record in self._student):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        new_record: StudentRecord = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        self._student.append(new_record)
        return new_record

    def select_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> list[StudentRecord]:

        if (
            student_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
        ):
            return self._student.copy()

        result: list[StudentRecord] = []

        for record in self._student:
            if student_id is not None and record[0] != student_id:
                continue

            if first_name is not None and record[1] != first_name:
                continue

            if second_name is not None and record[2] != second_name:
                continue

            if age is not None and record[3] != age:
                continue

            if sex is not None and record[4] != sex:
                continue

            result.append(record)      
        return result
    
    def update_record(
        self,
        student_id: int,  # Ищем студента по ID (так как он уникален)
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> StudentRecord | None:
        """Обновляет поля существующего студента по его student_id."""
        
        if age is not None and age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        for i, record in enumerate(self._student):
            # Находим нужную запись по уникальному ID
            if record[0] == student_id:
                # Берем старые значения, если новые не переданы (None)
                new_first_name = first_name.strip() if first_name is not None else record[1]
                new_second_name = second_name.strip() if second_name is not None else record[2]
                new_age = age if age is not None else record[3]
                new_sex = sex.strip() if sex is not None else record[4]
                updated_record: StudentRecord = (
                    student_id,
                    new_first_name,
                    new_second_name,
                    new_age,
                    new_sex,
                )
                
                self._student[i] = updated_record
                return updated_record
                
        # Если студента с таким ID не нашли
        return None

    def delete_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> int:
        """
        Удаляет записи, соответствующие переданным фильтрам.
        Возвращает количество удаленных записей.
        """
        # Если вообще ничего не передали — ничего не удаляем, чтобы случайно не стереть всю базу
        if (
            student_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
        ):
            return 0

        initial_count = len(self._student)
        remaining_students: list[StudentRecord] = []

        for record in self._student:
            # Твой родной алгоритм проверки: если поле передано и оно НЕ совпадает — 
            # значит, эта запись НЕ подлежит удалению, мы её сохраняем.
            if student_id is not None and record[0] != student_id:
                remaining_students.append(record)
                continue

            if first_name is not None and record[1] != first_name:
                remaining_students.append(record)
                continue

            if second_name is not None and record[2] != second_name:
                remaining_students.append(record)
                continue

            if age is not None and record[3] != age:
                remaining_students.append(record)
                continue

            if sex is not None and record[4] != sex:
                remaining_students.append(record)
                continue
            pass

        self._student = remaining_students
        deleted_count = initial_count - len(self._student)
        return deleted_count