import json
import os
import unittest
from unittest.mock import patch

from classes import Book
from engine_logic import (add_book, change_status, data_to_json, delete_book,
                          json_to_data, search)


class TestEngineLogic(unittest.TestCase):
    """Тестирование основной логики приложения."""

    def setUp(self):
        """
        Настройка перед каждым тестом.

        Создаем временный файл book.json.
        """
        self.test_file = "test_book.json"
        self.sample_books = [
            Book(1, "Книга 1", "Автор 1", "2000", "В наличии"),
            Book(2, "Книга 2", "Автор 2", "2010", "Выдана"),
        ]
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.sample_books],
                file, indent=4
            )

    def tearDown(self):
        """Удаляем тестовый файл после каждого теста."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch("engine_logic.database", "test_book.json")
    def test_a_json_to_data(self):
        """Тест загрузки данных из JSON в список объектов Book."""
        books = json_to_data()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Книга 1")
        self.assertEqual(books[1].status, "Выдана")

    @patch("engine_logic.database", "test_book.json")
    def test_b_data_to_json(self):
        """Тест сохранения списка объектов Book в JSON файл."""
        new_books = [
            Book(3, "Книга 3", "Автор 3", "2020", "В наличии"),
            Book(4, "Книга 4", "Автор 4", "2021", "Выдана"),
        ]
        data_to_json(new_books)
        with open(self.test_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Книга 3")
        self.assertEqual(data[1]["status"], "Выдана")

    @patch("engine_logic.database", "test_book.json")
    @patch("builtins.input", side_effect=["Книга 3", "Автор 3", "2020"])
    def test_c_add_book(self, mock_input):
        """Тест добавления книги в базу данных."""
        add_book()
        books = json_to_data()
        self.assertEqual(len(books), 3)
        self.assertEqual(books[-1].title, "Книга 3")

    @patch("builtins.input", side_effect=["1", "y"])
    @patch("engine_logic.database", "test_book.json")
    def test_d_delete_book(self, mock_input):
        """Тест удаления книги по ID."""
        delete_book()
        books = json_to_data()
        self.assertEqual(len(books), 1)
        self.assertNotEqual(books[0].id, "1")

    @patch("engine_logic.database", "test_book.json")
    @patch("builtins.input", side_effect=["1"])
    def test_e_change_status(self, mock_input):
        """Тест изменения статуса книги."""
        change_status()
        books = json_to_data()
        self.assertEqual(books[0].status, "Выдана")

    @patch("engine_logic.database", "test_book.json")
    @patch("builtins.input", side_effect=["1", "Книга 1"])
    def test_f_search_by_title(self, mock_input):
        """Тест поиска книги по названию."""
        search()
        books = json_to_data()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Книга 1")

    @patch("engine_logic.database", "test_book.json")
    @patch("builtins.input", side_effect=["2", "Автор 2"])
    def test_g_search_by_author(self, mock_input):
        """Тест поиска книги по автору."""
        search()
        books = json_to_data()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[1].author, "Автор 2")

    @patch("engine_logic.database", "test_book.json")
    @patch("builtins.input", side_effect=["3", "2010"])
    def test_h_search_by_year(self, mock_input):
        """Тест поиска книги по году издания."""
        search()
        books = json_to_data()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[1].year, "2010")
