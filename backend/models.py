from pydantic import BaseModel, Field
from typing import Optional, List

#Validate model for books
class Book(BaseModel):
    id: Optional[int] 
    isbn: Optional[str]
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    publication_year: Optional[int] = Field(default=None, le=2026)
    status: Optional[str] = "Pending"

#Validation model for book data for submitted forms
class BookForm(BaseModel):
    isbn: Optional[str]
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    publication_year: Optional[int] = Field(default=None, le=2026)

class SearchResult(BaseModel):
    isbn: Optional[str]
    title: str = ""
    author: str = ""
    publication_year: Optional[int] = Field(default=None, le=2026)
