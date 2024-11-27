from engine_logic import (add_book, all_books, change_status, delete_book,
                          search, to_main_menu)


def main():
    """
    Основная функция программы.

    Предоставляет пользователю интерфейс для взаимодействия с библиотекой:
    добавление, удаление, поиск книг, отображение всех книг,
    изменение статуса книги. Цикл продолжается до тех пор,
    пока пользователь не выберет опцию выхода.
    """
    while True:
        print("\nДобро пожаловать в библиотеку!")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input()
        if choice == "1":
            add_book()
            to_main_menu()
        if choice == "2":
            delete_book()
            to_main_menu()
        if choice == "3":
            search()
            to_main_menu()
        if choice == "4":
            all_books()
            to_main_menu()
        if choice == "5":
            change_status()
            to_main_menu()
        if choice == "6":
            print("До свидания!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем. До свидания!")
