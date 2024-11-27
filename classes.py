class Book:
    """
    Инициализирует объект книги.

    Args:
        id (str): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (str): Год издания книги.
        status (str): Статус книги (например, 'В наличии', 'Выдана').
    """

    def __init__(
        self, id: str, title: str, author: str, year: str, status: str
    ) -> None:
        self.id: str = id
        self.title: str = title
        self.author: str = author
        self.year: str = year
        self.status: str = status

    def to_dict(self) -> dict[str, str]:
        """
        Преобразует объект книги в словарь для хранения в JSON.

        Returns:
            dict: Словарь, представляющий объект книги с полями
                'id', 'title', 'author', 'year', 'status'.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict[str, str]) -> "Book":
        """
        Преобразует словарь в объект книги.

        Args:
            data (dict): Словарь, содержащий данные книги с полями
                'id', 'title', 'author', 'year', 'status'.

        Returns:
            Book: Объект книги, созданный на основе данных из словаря.
        """
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )
