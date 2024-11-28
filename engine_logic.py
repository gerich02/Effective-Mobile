import json
import os
from datetime import datetime

from classes import Book
from constants import (BLUE, DATABASE, GREEN, MIN_YEAR, RED, RESET, SEPARATOR,
                       STATUS_AVAILABLE, STATUS_ISSUED)


def json_to_data() -> list[Book]:
    """
    Преобразует Json в список экземпляров класса Book.

    Если файл отсутствует, создается пустой файл JSON.
    Returns:
        list: Список объектов класса Book.
    """
    try:
        if not os.path.exists(DATABASE):
            with open(DATABASE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
        with open(DATABASE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Book.from_dict(book) for book in data]
    except FileNotFoundError as e:
        print(
            f"{RED}Ошибка: Файл {RESET}'{DATABASE}' {RED}не найден. {RESET}{e}"
        )
        to_main_menu()
    except json.JSONDecodeError as e:
        print(f"{RED}Ошибка: Невозможно разобрать файл JSON. {RESET}{e}")
        to_main_menu()
    except TypeError as e:
        print(f"{RED}Ошибка: Некорректные данные в JSON. {RESET}{e}")
        to_main_menu()
    except Exception as e:
        print(f"{RED}Неизвестная ошибка: {RESET}{e}")
        to_main_menu()


def data_to_json(books: list[Book]) -> None:
    """
    Сохраняет список объектов Book в JSON файл.

    Args:
        books (list): Список объектов класса Book.
    """
    try:
        with open(DATABASE, "w", encoding="utf-8") as file:
            json.dump(
                [
                    book.to_dict() for book in books
                ],
                file, indent=4,
                ensure_ascii=False
            )
    except FileNotFoundError:
        print(
            f"{RED}Ошибка: Директория для файла {RESET}"
            f"{DATABASE} {RED}не найдена.{RESET}"
        )
        to_main_menu()
    except PermissionError:
        print(
            f"{RED}Ошибка: У вас нет прав на запись в файл {RESET}{DATABASE}."
        )
        to_main_menu()
    except TypeError as e:
        print(f"{RED}Ошибка при сериализации данных: {RESET}{e}")
        to_main_menu()
    except IOError as e:
        print(f"{RED}Ошибка ввода-вывода: {RESET}{e}")
        to_main_menu()
    except OSError as e:
        print(f"{RED}Ошибка операционной системы: {RESET}{e}")
        to_main_menu()
    except Exception as e:
        print(f"{RED}Произошла непредвиденная ошибка: {RESET}{e}")
        to_main_menu()


def id_generator() -> str:
    """
    Генерирует уникальный ID для новой книги на основе последнего ID в списке.

    Returns:
        str: Новый уникальный ID.
    """
    try:
        books = json_to_data()
        if books:
            return int(books[-1].id) + 1
        return 1
    except FileNotFoundError:
        print(f"{RED}Файл базы данных не найден.{RESET}")
        to_main_menu()
    except json.JSONDecodeError:
        print(
            f"{RED}Ошибка в формате JSON файла. {RESET}"
            f"{RED}Проверьте целостность базы.{RESET}"
        )
        to_main_menu()
    except (ValueError, IndexError):
        print(
            f"О{RED}шибка при генерации ID. {RESET}"
            f"{RED}Проверьте целостность данных.{RESET}"
        )
        to_main_menu()


def to_main_menu():
    """Возврат в главное меню."""
    print(f"\n{SEPARATOR}")
    print(f"\n{BLUE}Желаете продолджить? {RESET}")
    print(f"{BLUE}1. В главное меню{RESET}")
    print(f"{BLUE}2. выход{RESET}")
    while True:
        choice = input(f"{BLUE}Введите ваш выбор: {RESET}")
        print(f"\n{SEPARATOR}")
        if choice == "1":
            return
        if choice == "2":
            print(f"{GREEN}До свидания{BLUE}")
            exit()
        print(
            f"{RED}Неверный ввод, {RESET}"
            f"{RED}выберите один из предложенных вариантов.{RESET}"
        )


def add_book() -> None:
    """
    Добавляет новую книгу в базу данных.

    Сохраняет изменения в JSON файл.
    """
    try:
        books = json_to_data()
    except Exception as e:
        print(f"{RED}Ошибка при загрузке базы данных: {RESET}{e}")
        to_main_menu()
        return
    book_id = id_generator()
    while True:
        title = input(f"{BLUE}Введите название книги:{RESET}")
        if 2 <= len(title) <= 250:
            break
        print(
            f"{RED}Название книги должно быть от 2 до 250 символов.{RESET}"
            f"{RED}Попробуйте снова.{RESET}"
        )
    while True:
        author = input(f"{BLUE}Введите имя автора:{RESET}")
        if len(author) <= 250:
            break
        print(
            f"{RED}Имя не может превышать 250 символов. {RESET}"
            f"{RED}Попробуйте снова.{RESET}"
        )
    while True:
        year = input(f"{BLUE}Введите год издания:{RESET}")
        try:
            if MIN_YEAR <= int(year) <= datetime.now().year:
                break
            print(
                f"{RED}Год не может быть больше {RESET}"
                f"{RED}текущего или меньше {MIN_YEAR}.{RESET}"
                f"{RED}Попробуйте снова:{RESET}"
            )
        except ValueError:
            print(f"{RED}Введите корректное число.{RESET}")
    status = STATUS_AVAILABLE
    new_book = Book(book_id, title, author, year, status)
    books.append(new_book)
    data_to_json(books)
    print(
        f"{GREEN}Книга {RESET}'{new_book.title}'"
        f"{GREEN} добавлена с ID {new_book.id}!{RESET}"
    )


def delete_book() -> None:
    """
    Удаляет книгу из базы данных по ID.

    Сохраняет изменения в JSON файл.
    """
    try:
        books = json_to_data()
    except Exception as e:
        print(f"{RED}Ошибка при загрузке базы данных: {RESET}{e}")
        to_main_menu()
        return
    if not books:
        print(f"{RED}База данных пуста. Удаление невозможно.{RESET}")
        return
    delete_id = input(f"{BLUE}Введите ID книги для удаления: {RESET}")
    initial_count = len(books)
    books = [book for book in books if book.id != int(delete_id)]
    confirm = input(
        f"{BLUE}Вы уверены, что хотите удалить книгу с ID {RESET}"
        f"{RED}{delete_id}? {RED}(y/n):{RESET} "
    )
    if confirm.lower() != 'y':
        print(f"{GREEN}Удаление отменено.{RESET}")
        return
    if len(books) < initial_count:
        data_to_json(books)
        print(
            f"{GREEN}Книга с ID {RESET}{delete_id}"
            f"{GREEN} успешно удалена.{RESET}"
        )
    else:
        print(f"{RED}Книга с ID {RESET}{delete_id}{RED} не найдена.{RESET}")


def search() -> None:
    """
    Осуществляет поиск книги в базе данных.

    Поиск осуществляется по выбранному параметру:
    названию, автору или году издания.
    Выводит результаты поиска в консоль.
    """
    try:
        books = json_to_data()
    except Exception as e:
        print(f"{RED}Ошибка при загрузке базы данных: {RESET}{e}")
        to_main_menu()
        return
    if not books:
        print(f"{RED}База данных пуста. Поиск невозможен.{RESET}")
        return
    print(f"{BLUE}По какому параметру будем осуществлять поиск?{RESET}")
    print(f"{BLUE}1. По названию{RESET}")
    print(f"{BLUE}2. По автору{RESET}")
    print(f"{BLUE}3. По году{RESET}")
    while True:
        search_parameter: str = input(
            f"{BLUE}Введите номер параметра поиска: {RESET}"
        )
        if search_parameter in {"1", "2", "3"}:
            break
        print(f"{RED}Некорректный выбор параметра. Попробуйте снова.{RESET}")
    while True:
        search_value: str = input(f"{BLUE}Введите занчение поиска: {RESET}")
        if search_parameter in {"1", "2"} and search_value:
            break
        try:
            if MIN_YEAR <= int(search_value) <= datetime.now().year:
                break
            print(
                f"{RED}Год не может быть больше {RESET}"
                f"{RED}текущего или меньше {MIN_YEAR}. {RESET}"
                f"{RED}Попробуйте снова:{RESET}"
            )
        except ValueError:
            print(
                f"{RED}Введите корректный год:"
                f"(от {MIN_YEAR} до текущего).{RESET}"
            )
    if search_parameter == "1":
        filtred_books = [
            book for book in books
            if search_value.lower() in book.title.lower()
        ]
    elif search_parameter == "2":
        filtred_books = [
            book for book in books
            if search_value.lower() in book.author.lower()
        ]
    elif search_parameter == "3":
        filtred_books = [
            book for book in books
            if book.year == search_value
        ]
    if filtred_books:
        print(f"\n{SEPARATOR}")
        print(f"{BLUE}Результаты поиска: {RESET}")
        for book in filtred_books:
            print(f"{GREEN}ID: {book.id}{RESET}")
            print(f"{BLUE}Название:{RESET} {book.title}")
            print(f"{BLUE}Автор:{RESET} {book.author}")
            print(f"{BLUE}Год издания:{RESET} {book.year}")
            print(f"{BLUE}Наличие:{RESET} {book.status}")
            print(f"{SEPARATOR}")
    else:
        print("Совпадений не найдено.")


def all_books() -> None:
    """Выводит в консоль список всех книг и параметров из базы данных."""
    try:
        books = json_to_data()
    except Exception as e:
        print(f"Ошибка при загрузке базы данных: {e}")
        to_main_menu()
        return
    for book in books:
        print(f"\n{SEPARATOR}")
        print(f"{GREEN}ID: {book.id}{RESET}")
        print(f"{BLUE}Название:{RESET} {book.title}")
        print(f"{BLUE}Автор:{RESET} {book.author}")
        print(f"{BLUE}Год издания:{RESET} {book.year}")
        print(f"{BLUE}Наличие:{RESET} {book.status}")
        print(f"{SEPARATOR}\n")


def change_status() -> None:
    """
    Изменяет статус книги по её ID.

    Если статус был 'В наличии', меняется на 'Выдана' и наоборот.
    Сохраняет изменения в JSON файл.
    """
    try:
        books = json_to_data()
    except Exception as e:
        print(f"{RED}Ошибка при загрузке базы данных: {RESET}{e}")
        to_main_menu()
        return
    while True:
        change_id = input(f"{BLUE}Введите ID книги:{RESET}")
        try:
            if 1 <= int(change_id):
                break
            print(
                f"{RED}Id не может быть больше меньше 1.{RESET}"
                f"{RED}Попробуйте снова:{RESET}"
            )
        except ValueError:
            print(f'{RED}Введите корректное число.{RESET}')
    try:
        book = next(book for book in books if book.id == int(change_id))
    except StopIteration:
        print(f"\n{SEPARATOR}")
        print(f"{RED}Книга с ID {RESET}{change_id} {RED}не найдена.{RESET}")
        print(f"\n{SEPARATOR}")
        return
    if book.status == STATUS_AVAILABLE:
        book.status = STATUS_ISSUED
        print(f"\n{SEPARATOR}")
        print(
            f"{GREEN}Статус книги с ID{RESET} {change_id} "
            f"{GREEN}изменен на {RESET}'{book.status}'.")
        print(f"\n{SEPARATOR}")
    else:
        book.status = STATUS_AVAILABLE
        print(f"\n{SEPARATOR}")
        print(
            f"{GREEN}Статус книги с ID{RESET} {change_id} "
            f"{GREEN}изменен на {RESET}'{book.status}'.")
        print(f"\n{SEPARATOR}")
    data_to_json(books)
