from src.db.backend.file import FileDatabase
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import DatabaseError

class TUI:
    def __init__(self) -> None:
        print("Выберите тип базы данных:")
        print("1. In-memory")
        print("2. File database")

        choice = input("Введите номер: ").strip()
        if choice == "2":
            self.database = FileDatabase()
        else:
            self.database = MemoryDatabase()
            
        self.table_name = "students"
            
        try:
            self.database.create_table(self.table_name, ("student_id", "first_name", "second_name", "age", "sex"))
        except DatabaseError:
            pass

    def main_menu(self) -> None:
        while True:
            print("\n1. Добавить 2. Показать 3. Найти по фильтру 4. Изменить 5. Удалить 0. Выход")
            choice = input("Действие: ").strip()

            try:
                if choice == "1":
                    record = {
                        "student_id": int(input("ID: ")),
                        "first_name": input("Имя: "),
                        "second_name": input("Фамилия: "),
                        "age": int(input("Возраст: ")),
                        "sex": input("Пол: ")
                    }
                    self.database.insert_record(self.table_name, record)
                    print("Запись успешно добавлена!")
                    
                elif choice == "2":
                    records = self.database.select_records(self.table_name)
                    for r in records:
                        print(r)
                        
                elif choice == "3":
                    key = input("Введите имя поля для фильтра (например, first_name): ").strip()
                    val = input("Введите значение: ").strip()
                    if key in ("student_id", "age"):
                        val = int(val) # type: ignore
                    
                    filters = {key: val} if key else {}
                    records = self.database.select_records(self.table_name, **filters)
                    for r in records:
                        print(r)

                elif choice == "4":
                    print("--- Изменение записи ---")
                    student_id = int(input("Введите ID студента для изменения: "))
                    
                    print("Введите новые данные (оставьте пустым, если не хотите менять):")
                    new_name = input("Новое имя: ").strip()
                    new_last = input("Новая фамилия: ").strip()
                    new_age = input("Новый возраст: ").strip()
                    new_sex = input("Новый пол: ").strip()
                    
                    update_data = {}
                    if new_name: update_data["first_name"] = new_name
                    if new_last: update_data["second_name"] = new_last
                    if new_age: update_data["age"] = int(new_age)
                    if new_sex: update_data["sex"] = new_sex
                    
                    if update_data:
                        self.database.update_records(self.table_name, update_data, student_id=student_id)
                        print("Запись успешно обновлена!")
                    else:
                        print("Изменения не внесены (поля пустые).")

                elif choice == "5":
                    print("--- Удаление записи ---")
                    student_id = int(input("Введите ID студента для удаления: "))
                    
                    self.database.delete_records(self.table_name, student_id=student_id)
                    print("Запись успешно удалена!")
                    
                elif choice == "0":
                    print("До свидания!")
                    break
            except Exception as e:
                print(f"Ошибка: {e}")

def run():
    ui = TUI()
    ui.main_menu()

if __name__ == "__main__":
    run()
