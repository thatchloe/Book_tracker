# models.py
from typing import Optional

class BookDB:
    """Represents how a book exists in the database."""
    def __init__(
        self,
        id: int,
        isbn: Optional[str],
        title: str,
        author: str,
        publication_year: Optional[int],
        status: str = "Pending",
    ):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.status = status
