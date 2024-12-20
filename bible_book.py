from constants import RESET, YELLOW
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
        print(f"\n{YELLOW}Добро пожаловать в библиотеку!{RESET}")
        print(f"{YELLOW}1. Добавить книгу{RESET}")
        print(f"{YELLOW}2. Удалить книгу{RESET}")
        print(f"{YELLOW}3. Искать книгу{RESET}")
        print(f"{YELLOW}4. Показать все книги{RESET}")
        print(f"{YELLOW}5. Изменить статус книги{RESET}")
        print(f"{YELLOW}6. Выйти{RESET}")
        choice = input()
        if choice == "1":
            add_book()
            to_main_menu(add_book)
        if choice == "2":
            delete_book()
            to_main_menu(delete_book)
        if choice == "3":
            search()
            to_main_menu(search)
        if choice == "4":
            all_books()
            to_main_menu(all_books)
        if choice == "5":
            change_status()
            to_main_menu(change_status)
        if choice == "6":
            print(f"{YELLOW}До свидания!{RESET}")
            break


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Программа приостановлена. Возврат в главное меню...{RESET}")
            to_main_menu()
