from .backend.memory import StudentTable
from .backend.errors import StudentTableError

def main_menu():
    db = StudentTable()

    while True:
        print("\n1. Добавить 2. Показать 3. Обновить 4. Удалить 0. Выход")
        choice = input("Действие: ").strip()

        try:
            if choice == "1":
                db.create_record(
                    int(input("ID: ")),
                    input("Имя: "),
                    input("Фамилия: "),
                    int(input("Возраст: ")),
                    input("Пол: "),
                )
            elif choice == "2":
                for r in db.select_record():
                    print(r)
            elif choice == "3":
                db.update_record(
                    int(input("ID: ")),
                    input("Имя: "),
                    input("Фамилия: "),
                    int(input("Возраст: ")),
                    input("Пол: "),
                )
            elif choice == "4":
                db.delete_record(int(input("ID для удаления: ")))
            elif choice == "0":
                print("До свидания!")
                break
        except (ValueError, StudentTableError) as e:
            print(f"Ошибка: {e}")

def run():
    """Эта функция нужна для теста test_main.py"""
    main_menu()

if __name__ == "__main__":
    run()
