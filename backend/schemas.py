# schemas.py
from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    isbn: Optional[str] = None
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    publication_year: Optional[int] = Field(default=None, le=2026)


# POST /books
class BookCreate(BookBase):
    pass


# PUT/PATCH /books/{id}
class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = Field(default=None, min_length=1)
    author: Optional[str] = Field(default=None, min_length=1)
    publication_year: Optional[int] = Field(default=None, le=2026)
    status: Optional[str] = None


# GET /books/{id}
class BookOut(BookBase):
    id: int
    status: str


# Search results (external or partial matches)
class SearchResult(BaseModel):
    isbn: Optional[str] = None
    title: str = ""
    author: str = ""
    publication_year: Optional[int] = Field(default=None, le=2026)
