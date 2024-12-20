# BIBLE BOOK for Effective-Mobile 

## Описание

Проект **Effective-Mobile** — это простое консольное приложение для управления библиотекой. Программа позволяет добавлять, удалять, изменять статус и искать книги по различным параметрам. Все данные о книгах сохраняются в JSON файл, который обновляется после каждого изменения. Интерфейс интуитивно понятный для рядового пользователя.

### Особенности
- Добавление, удаление, изменение статуса книг.
- Поиск книг по названию, автору или году издания.
- Все данные хранятся в JSON файле, что позволяет легко изменять или добавлять записи.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:gerich02/Effective-Mobile.git

## Запуск проекта в dev-режиме

- Склонируйте репозиторий:  
```git clone git@github.com:gerich02/Effective-Mobile.git ```    
- Перейдите в каталог проекта. Важно, чтобы все манипуляции проводились из корневой директории:  
``` cd Effective-Mobile ```  
- Убедитесь, что у вас установлен Python (3.x).
``` python --version ```
- Запустите проект командой:   
```python bible_book.py```

---
### Детализированное описание функционала


#### **1. Добавить книгу**
- **Описание**: Пользователь вводит данные о книге — название, автора и год издания. Программа проверяет введенные данные на корректность.
- **Ошибки**:
  - Если название книги пустое, выводится сообщение об ошибке.
  - Если автор книги не указан, программа запросит данные повторно.
  - Если год издания указан некорректно (например, содержит буквы или находится вне допустимого диапазона), программа уведомит пользователя и попросит ввести год заново.
- **Возврат в меню**:
  - После успешного добавления книги, пользователь может вернуться в главное меню, выйти или добавить еще одну книгу.

#### **2. Удалить книгу**
- **Описание**: Пользователь вводит ID книги, которую необходимо удалить.
- **Ошибки**:
  - Если ID не существует в базе данных, программа выводит сообщение о том, что книга с таким ID не найдена.
  - Если пользователь вводит некорректный формат ID (например, буквы вместо чисел), программа уведомляет о необходимости ввести число.
- **Возврат в меню**:
  - После успешного удаления книги (или после сообщения об ошибке), пользователь может вернуться в главное меню, выйти или повторить попытку удаления.


#### **3. Искать книгу**
- **Описание**: Программа позволяет искать книгу по одному из трех параметров: название, автор или год издания. Пользователь выбирает критерий поиска, вводит значение, и программа возвращает все подходящие результаты.
- **Ошибки**:
  - Если ни одна книга не соответствует запросу, программа уведомляет об этом.
  - Если пользователь вводит пустое значение для поиска, программа выводит сообщение о необходимости ввода данных.
- **Возврат в меню**:
  - После выполнения поиска пользователь может вернуться в главное меню, выйти или повторить поиск.


#### **4. Показать все книги**
- **Описание**: Программа выводит список всех книг, хранящихся в базе данных.
  - Для каждой книги отображается ID, название, автор, год издания и статус (например, "В наличии" или "Выдана").
- **Ошибки**:
  - Если база данных пуста, программа уведомляет пользователя, что книг пока нет.
- **Возврат в меню**:
  - После отображения списка пользователь может вернуться в главное меню, выйти или повторить запрос.


#### **5. Изменить статус книги**
- **Описание**: Пользователь вводит ID книги, а затем выбирает новый статус: "В наличии" или "Выдана".
- **Ошибки**:
  - Если введенный ID не существует, программа уведомляет пользователя об этом.
  - Если статус введен некорректно, программа просит выбрать один из допустимых вариантов.
- **Возврат в меню**:
  - После успешного изменения статуса (или сообщения об ошибке) пользователь может вернуться в главное меню, выйти или изменить статус другой книги.

#### **6. Выйти**
- **Описание**: Завершает работу программы.
  - Перед выходом программа автоматически сохраняет все изменения в файл `book.json`.


### Общие аспекты

#### **Возврат в главное меню**
- Возврат осуществляется по выбору пользователя после любой ошибки, не связанной с вводом команд.
- Для всех операций пользователю предоставляется возможность вручную вернуться в меню, выйти из программы или повторить выполнение последнего действия.
- Если же в каком то месте выполнения программы пользователь захочет вернуться в главное меню, добавленя обработка KeyboardInterrupt, при нажатии ctrl+C будет предложено либо вернуться в главное меню, либо выйти из программы.

#### **Обработка ошибок**
- Все пользовательские вводы проверяются на корректность:
  - Пустые строки или пробелы не принимаются.
  - Некорректные форматы данных (например, буквы вместо чисел) приводят к повторному запросу ввода.
  - При некорректном вводе данных пользователь получает сообщение с подсказкой, что было сделано неправильно. После чего дается возможность повторить ввод. При этом функция не запускается заново, а продолжает работать с того места, где была совершена ошибка.
- Если в ходе работы программы файл `book.json` отсутствует или поврежден, создается новый файл с пустой базой данных.


### Пример взаимодействия
- При вводе некорректных данных программа не завершает работу, а предлагает повторить ввод, позволяя пользователю исправить ошибку. Это упрощает использование и делает приложение более устойчивым к ошибкам. Так же приложение дает подсказки, если с первого раза у пользователя не получилось ввести корректные данные. В конце выполнения каждой функции приложения Вам будет предложено вернуться в главное меню, выйти из приложения или повторить последнее действие.
---

## Тестирование
В данном приложении содержатся тесты, реализованные при помощи встроенной в Python библиотеки unittest.
Для того, чтобы запустить их, их коневой директории проекта выполните команду:
```python -m unittest -b```

Данные тесты включают:
- тест загрузки данных из JSON в список объектов Book;
- тест сохранения списка объектов Book в JSON файл;
- тест добавления книги в базу данных;
- тест удаления книги по ID;
- тест изменения статуса книги;
- тест поиска книги по названию;
- тест поиска книги по автору;
- тест поиска книги по году издания.
---

## Файл данных

Вся информация о книгах хранится в файле book.json, который создается автоматически, если его нет в проекте.

---
## Структура проекта
- bible_book.py — Главный файл программы, содержит логику интерфейса и взаимодействия с пользователем;
- engine_logic.py — Логика обработки данных: добавление, удаление, поиск и обновление статуса книг;
- classes.py — Описание класса Book с методами для сериализации и десериализации данных;
- constants.py — Константы для форматирования текстового вывода в консоль, минмиальных значений и адреса БД;
- tests/tests.py - директория для хранения тестов;
- book.json - тестовая база данных в формате json.

---
## Об авторе
- [Варивода Георгий](https://github.com/gerich02)