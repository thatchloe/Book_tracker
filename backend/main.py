from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import httpx
from models import Book, BookForm
from helper import extract_data
from database import Database
from dotenv import load_dotenv
import os
from typing import List, Annotated


# Load environment variables
load_dotenv()


GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000"
]

# Allow the static frontend to call the API from any localhost port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


db = Database("books.db")


@app.get("/api/books/search")
async def search_books(query: str):
    """Search books using Google Books API"""
    try:

        params = {"q": query, "key": GOOGLE_BOOKS_API_KEY}

        # Call Google Books API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GOOGLE_BOOKS_API_URL, params=params, timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

        # Parse and return results
        results = extract_data(data)
        return results

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Error calling Google Books API: {str(e)}"
        )
    


@app.post("/api/books/save", response_model=Book)
async def save_book(data: BookForm):
    try:
        created_book = db.save_book(data)  # pass the model itself
        return created_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save book: {e}")



@app.get("/api/books", response_model=List[Book])
async def get_books():
    """Get all books
    """
    try:
        books = db.get_all_books()
        return books
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve books: {str(e)}"
        )


@app.put("/api/books/{book_id}", response_model=Book)
async def update_book(book_id: int):
    """
    Update a book status to Read (only if current status is Pending).
    """
   
    # Get the book first
    book = db.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = db.update_book(book_id)
    return updated_book

  


@app.delete("/api/books/{book_id}")
async def delete_book(book_id: int):
    """Delete a book entry"""
   
    deleted = db.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
