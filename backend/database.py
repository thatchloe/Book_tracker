"""
Database module for SQLite3 operations.
Handles all database connections and CRUD operations.
"""

import sqlite3
from typing import Optional, List
from models import BookDB
from schemas import BookCreate
from contextlib import contextmanager


class Database:
    """SQLite3 database manager."""

    def __init__(self, db_name: str = "books.db"):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER,
                    status TEXT NOT NULL DEFAULT 'Pending'
                )
                """
            )
            conn.commit()

    # CREATE
    def save_book(self, book_data: BookCreate) -> BookDB:
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO books (isbn, title, author, publication_year, status)
                VALUES (?, ?, ?, ?, 'Pending')
                """,
                (
                    book_data.isbn,
                    book_data.title,
                    book_data.author,
                    book_data.publication_year,
                ),
            )
            book_id = cursor.lastrowid
            conn.commit()

            row = conn.execute(
                "SELECT * FROM books WHERE id = ?", (book_id,)
            ).fetchone()

            return self._row_to_book(row)

    # READ ALL
    def get_all_books(self) -> List[BookDB]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM books ORDER BY id").fetchall()
            return [self._row_to_book(row) for row in rows]

    # READ ONE
    def get_book_by_id(self, book_id: int) -> Optional[BookDB]:
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM books WHERE id = ?", (book_id,)
            ).fetchone()
            return self._row_to_book(row) if row else None

    # UPDATE (status change only)
    def update_book(self, book_id: int) -> Optional[BookDB]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE books 
                SET status = 'Read'
                WHERE id = ? AND status = 'Pending'
                """,
                (book_id,),
            )

            conn.commit()
            if cursor.rowcount == 0:
                return None

            return self.get_book_by_id(book_id)

    # DELETE
    def delete_book(self, book_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM books WHERE id = ?", (book_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    # Convert DB row → internal model
    def _row_to_book(self, row: sqlite3.Row) -> BookDB:
        return BookDB(
            id=row["id"],
            isbn=row["isbn"],
            title=row["title"],
            author=row["author"],
            publication_year=row["publication_year"],
            status=row["status"],
        )
