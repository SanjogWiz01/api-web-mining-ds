"""
===============================================================================
Lesson 08: Full Production-Grade REST CRUD Application
===============================================================================
80/20 Principle Focus:
- Putting all previous concepts together into a complete CRUD REST API
- C: Create  (POST /api/v1/books/)
- R: Read    (GET /api/v1/books/ & GET /api/v1/books/{id})
- U: Update  (PUT & PATCH /api/v1/books/{id})
- D: Delete  (DELETE /api/v1/books/{id})
- Separate Pydantic schemas for Create, Update, and Response
- Clean status codes & 404 exception handling

How to Run:
   python 08_crud_application.py
Interactive Docs Test:
- Open http://127.0.0.1:8000/docs and test full CRUD operations!
===============================================================================
"""

from typing import Optional
from fastapi import FastAPI, HTTPException, status, Query, Path
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 08: Complete REST CRUD API",
    description="Full implementation of Create, Read, Update, Delete operations for a Book collection.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 1. Pydantic Schemas
# -----------------------------------------------------------------------------
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, example="Clean Code")
    author: str = Field(..., min_length=1, max_length=100, example="Robert C. Martin")
    year: int = Field(..., ge=1800, le=2030, example=2008)
    genre: str = Field(..., example="Software Engineering")


class BookCreate(BookBase):
    """Schema for creating a new book (inherits all BookBase fields)."""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book (all fields optional for PATCH)."""
    title: str | None = Field(None, min_length=1, max_length=150)
    author: str | None = Field(None, min_length=1, max_length=100)
    year: int | None = Field(None, ge=1800, le=2030)
    genre: str | None = Field(None)


class BookResponse(BookBase):
    """Schema returned to API clients (includes database `id`)."""
    id: int


# -----------------------------------------------------------------------------
# 2. In-Memory Database State
# -----------------------------------------------------------------------------
BOOKS_DATABASE: dict[int, dict] = {
    1: {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999, "genre": "Software"},
    2: {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "year": 2017, "genre": "Data Science"},
    3: {"id": 3, "title": "Fluent Python", "author": "Luciano Ramalho", "year": 2022, "genre": "Python"},
}
id_counter = 3


# -----------------------------------------------------------------------------
# 3. CRUD Endpoints
# -----------------------------------------------------------------------------

# READ ALL (List & Search & Paginate)
@app.get(
    "/api/v1/books/",
    response_model=list[BookResponse],
    summary="List and filter books",
)
def get_books(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Page limit"),
    genre: str | None = Query(None, description="Optional genre filter"),
):
    """Retrieve books with optional pagination and genre filtering."""
    books = list(BOOKS_DATABASE.values())

    if genre:
        books = [b for b in books if b["genre"].lower() == genre.lower()]

    return books[skip : skip + limit]


# READ SINGLE
@app.get(
    "/api/v1/books/{book_id}",
    response_model=BookResponse,
    summary="Get book by ID",
)
def get_book_by_id(book_id: int = Path(..., gt=0)):
    """Fetch a single book by ID or return 404 if not found."""
    if book_id not in BOOKS_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found.",
        )
    return BOOKS_DATABASE[book_id]


# CREATE
@app.post(
    "/api/v1/books/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new book",
)
def create_book(book_in: BookCreate):
    """Add a new book to the catalog."""
    global id_counter
    id_counter += 1

    new_book = {"id": id_counter, **book_in.model_dump()}
    BOOKS_DATABASE[id_counter] = new_book
    return new_book


# UPDATE (PUT - Full Replace)
@app.put(
    "/api/v1/books/{book_id}",
    response_model=BookResponse,
    summary="Replace entire book entity",
)
def replace_book(book_id: int, book_in: BookCreate):
    """Completely overwrite an existing book's details."""
    if book_id not in BOOKS_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found.",
        )

    updated_book = {"id": book_id, **book_in.model_dump()}
    BOOKS_DATABASE[book_id] = updated_book
    return updated_book


# UPDATE (PATCH - Partial Update)
@app.patch(
    "/api/v1/books/{book_id}",
    response_model=BookResponse,
    summary="Partially update book attributes",
)
def update_book_partial(book_id: int, book_in: BookUpdate):
    """Update only specified fields of a book."""
    if book_id not in BOOKS_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found.",
        )

    stored_book = BOOKS_DATABASE[book_id]
    # Get only fields explicitly provided in request
    update_data = book_in.model_dump(exclude_unset=True)

    stored_book.update(update_data)
    BOOKS_DATABASE[book_id] = stored_book
    return stored_book


# DELETE
@app.delete(
    "/api/v1/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
)
def delete_book(book_id: int = Path(..., gt=0)):
    """Delete a book from the catalog."""
    if book_id not in BOOKS_DATABASE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found.",
        )
    del BOOKS_DATABASE[book_id]
    return None


if __name__ == "__main__":
    uvicorn.run("08_crud_application:app", host="127.0.0.1", port=8000, reload=True)
