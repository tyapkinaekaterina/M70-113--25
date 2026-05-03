
type StudentRecord = tuple[int, str, str, int, str]

Student: list[StudentRecord] = []


def create_record(
    student_id: int,   # Уникальный идентификатор записи
    first_name: str,   # Имя
    second_name: str,  # Фамилия
    age: int,          # Возраст
    sex: str,          # Пол
) -> StudentRecord:
    if age < 0:
        raise ValueError("Поле age не может быть отрицательным.")

    if any(record[0] == student_id for record in Student):
        raise ValueError(f"Запись с id={student_id} уже существует.")

    new_record: StudentRecord = (
        student_id,
        first_name.strip(),
        second_name.strip(),
        age,
        sex.strip(),
    )

    Student.append(new_record)

    return new_record


def select_record(
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
        return Student.copy()

    result: list[StudentRecord] = []

    for record in Student:
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
    student_id: int,
    first_name: str | None = None,
    second_name: str | None = None,
    age: int | None = None,
    sex: str | None = None,
) -> StudentRecord:
    
    target_index = None
    target_record = None
    
    for index, record in enumerate(Student):
        if record[0] == student_id:
            target_index = index
            target_record = record
            break
            
    if target_index is None:
        raise ValueError(f"Запись с id={student_id} не найдена.")
        
    new_first_name = first_name.strip() if first_name is not None else target_record[1]
    new_second_name = second_name.strip() if second_name is not None else target_record[2]
    
    if age is not None:
        if age < 0:
            raise ValueError("Поле age не может быть отрицательным.")
        new_age = age
    else:
        new_age = target_record[3]
        
    new_sex = sex.strip() if sex is not None else target_record[4]
    
    updated_record: StudentRecord = (
        student_id,
        new_first_name,
        new_second_name,
        new_age,
        new_sex,
    )
    
    Student[target_index] = updated_record
    
    return updated_record


def delete_record(student_id: int) -> StudentRecord:
    
    for index, record in enumerate(Student):
        if record[0] == student_id:
            return Student.pop(index)
            
    raise ValueError(f"Запись с id={student_id} не найдена для удаления.")
