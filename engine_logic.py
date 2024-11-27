import json
import os
from datetime import datetime

from classes import Book

database = "book.json"


def json_to_data() -> list[Book]:
    """
    Преобразует Json в список экземпляров класса Book.

    Если файл отсутствует, создается пустой файл JSON.
    Returns:
        list: Список объектов класса Book.
    """
    try:
        if not os.path.exists(database):
            with open(database, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
        with open(database, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Book.from_dict(book) for book in data]
    except FileNotFoundError as e:
        print(f"Ошибка: Файл '{database}' не найден. {e}")
        to_main_menu()
    except json.JSONDecodeError as e:
        print(f"Ошибка: Невозможно разобрать файл JSON. {e}")
        to_main_menu()
    except TypeError as e:
        print(f"Ошибка: Некорректные данные в JSON. {e}")
        to_main_menu()
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        to_main_menu()


def data_to_json(books: list[Book]) -> None:
    """
    Сохраняет список объектов Book в JSON файл.

    Args:
        books (list): Список объектов класса Book.
    """
    try:
        with open(database, "w", encoding="utf-8") as file:
            json.dump(
                [
                    book.to_dict() for book in books
                ],
                file, indent=4,
                ensure_ascii=False
            )
    except FileNotFoundError:
        print(f"Ошибка: Директория для файла {database} не найдена.")
        to_main_menu()
    except PermissionError:
        print(f"Ошибка: У вас нет прав на запись в файл {database}.")
        to_main_menu()
    except TypeError as e:
        print(f"Ошибка при сериализации данных: {e}")
        to_main_menu()
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
        to_main_menu()
    except OSError as e:
        print(f"Ошибка операционной системы: {e}")
        to_main_menu()
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
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
        print("Файл базы данных не найден.")
        to_main_menu()
    except json.JSONDecodeError:
        print("Ошибка в формате JSON файла. Проверьте целостность базы.")
        to_main_menu()
    except (ValueError, IndexError):
        print("Ошибка при генерации ID. Проверьте целостность данных.")
        to_main_menu()


def to_main_menu():
    """Возврат в главное меню."""
    print("\nЖелаете продолджить? ")
    print("1. В главное меню")
    print("2. выход")
    while True:
        choice = input("Введите ваш выбор: ")
        if choice == "1":
            return
        if choice == "2":
            print("До свидания")
            exit()
        print("Неверный ввод, выберите один из предложенных вариантов.")


def add_book() -> None:
    """
    Добавляет новую книгу в базу данных.

    Сохраняет изменения в JSON файл.
    """
    books = json_to_data()
    book_id = id_generator()
    while True:
        title = input("Введите название книги:")
        if 2 <= len(title) <= 250:
            break
        print(
            'Название книги должно быть от 2 до 250 символов.'
            'Попробуйте снова.'
        )
    while True:
        author = input("Введите имя автора:")
        if len(author) <= 250:
            break
        print('Имя не может превышать 250 символов. Попробуйте снова.')
    while True:
        year = input("Введите год издания:")
        try:
            if 1000 <= int(year) <= datetime.now().year:
                break
            print(
                'Год не может быть больше текущего или меньше 1000.'
                'Попробуйте снова:'
            )
        except ValueError:
            print('Введите корректное число.')
    status = "В наличии"
    new_book = Book(book_id, title, author, year, status)
    books.append(new_book)
    data_to_json(books)
    print(f"Книга '{new_book.title}' добавлена с ID {new_book.id}!")


def delete_book() -> None:
    """
    Удаляет книгу из базы данных по ID.

    Сохраняет изменения в JSON файл.
    """
    books = json_to_data()
    if not books:
        print("База данных пуста. Удаление невозможно.")
        return
    delete_id = input("Введите ID книги для удаления: ")
    initial_count = len(books)
    books = [book for book in books if book.id != int(delete_id)]
    confirm = input(
        f"Вы уверены, что хотите удалить книгу с ID {delete_id}? (y/n): "
    )
    if confirm.lower() != 'y':
        print("Удаление отменено.")
        return
    if len(books) < initial_count:
        data_to_json(books)
        print(f"Книга с ID {delete_id} успешно удалена.")
    else:
        print(f"Книга с ID {delete_id} не найдена.")


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
        print(f"Ошибка при загрузке базы данных: {e}")
        to_main_menu()
        return
    if not books:
        print("База данных пуста. Поиск невозможен.")
        return
    print("По какому параметру будем осуществлять поиск?")
    print("1. По названию")
    print("2. По автору")
    print("3. По году")
    while True:
        search_parameter: str = input("Введите номер параметра поиска: ")
        if search_parameter in {"1", "2", "3"}:
            break
        print("Некорректный выбор параметра. Попробуйте снова.")
    while True:
        search_value: str = input("Введите занчение поиска: ")
        if search_parameter in {"1", "2"} and search_value:
            break
        try:
            if 1000 <= int(search_value) <= datetime.now().year:
                break
            print(
                'Год не может быть больше текущего или меньше 1000. '
                'Попробуйте снова:'
            )
        except ValueError:
            print("Введите корректный год (от 1000 до текущего).")
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
        print("Результаты поиска: ")
        for book in filtred_books:
            print(
                f"\nId: {book.id}"
                f"\nНазвание: {book.title}"
                f"\nАвтор: {book.author}"
                f"\nГод издания: {book.year}"
                f"\nНаличие: {book.status}"
            )
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
        print(
            f"\nId: {book.id}"
            f"\nНазвание: {book.title}"
            f"\nАвтор: {book.author}"
            f"\nГод издания: {book.year}"
            f"\nНаличие: {book.status}"
        )


def change_status() -> None:
    """
    Изменяет статус книги по её ID.

    Если статус был 'В наличии', меняется на 'Выдана' и наоборот.
    Сохраняет изменения в JSON файл.
    """
    try:
        books = json_to_data()
    except Exception as e:
        print(f"Ошибка при загрузке базы данных: {e}")
        to_main_menu()
        return
    while True:
        change_id = input("Введите ID книги:")
        try:
            if 1 <= int(change_id):
                break
            print(
                'Id не может быть больше меньше 1.'
                'Попробуйте снова:'
            )
        except ValueError:
            print('Введите корректное число.')
    try:
        book = next(book for book in books if book.id == int(change_id))
    except StopIteration:
        print(f"Книга с ID {change_id} не найдена.")
        return
    if book.status == "В наличии":
        book.status = "Выдана"
        print(f"Статус книги с ID {change_id} изменен на '{book.status}'.")
    else:
        book.status = "В наличии"
        print(f"Статус книги с ID {change_id} изменен на '{book.status}'.")
    data_to_json(books)
