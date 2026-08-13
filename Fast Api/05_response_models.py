"""
===============================================================================
Lesson 05: Response Models, Filtering & HTTP Status Codes
===============================================================================
80/20 Principle Focus:
- Using `response_model` to define and enforce API output structure
- Hiding sensitive data (passwords, private metrics) from API responses
- Setting exact HTTP status codes (`status.HTTP_201_CREATED`, `204_NO_CONTENT`)
- Filtering default values using `response_model_exclude_unset=True`

How to Run:
   python 05_response_models.py
Test URLs:
- User Public Profile: http://127.0.0.1:8000/users/1
- Filtered Response:   http://127.0.0.1:8000/items/1
===============================================================================
"""

from typing import Optional
from fastapi import FastAPI, status, Response
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 05: Response Models & Status Codes",
    description="Learn how to filter outgoing data and set proper HTTP status codes.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 1. Models for Inbound Request vs Outbound Response
# -----------------------------------------------------------------------------
# Input schema (User registration payload containing plaintext password)
class UserIn(BaseModel):
    username: str
    email: str
    password: str  # Sensitive field!


# Output schema (Public user profile - NO password field!)
class UserOut(BaseModel):
    username: str
    email: str
    is_active: bool = True


# Internal DB representation
FAKE_USER_DB = {
    1: {"username": "alice", "email": "alice@example.com", "password": "supersecretpassword123", "is_active": True}
}


# -----------------------------------------------------------------------------
# 2. Hiding Sensitive Data with response_model & HTTP 201 Created
# -----------------------------------------------------------------------------
@app.post(
    "/users/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def create_user(user: UserIn):
    """
    Even though `user` includes a password, FastAPI filters the response through `UserOut`.
    The `password` key will NEVER be returned in the JSON response!
    """
    # Simulate saving to database
    new_user_id = len(FAKE_USER_DB) + 1
    FAKE_USER_DB[new_user_id] = user.model_dump()

    # We can safely return the internal dict containing password; FastAPI filters it automatically!
    return user.model_dump()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """Fetch user profile without exposing password."""
    user = FAKE_USER_DB.get(user_id)
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return user


# -----------------------------------------------------------------------------
# 3. Omitting Unset Defaults using response_model_exclude_unset
# -----------------------------------------------------------------------------
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True,
)
def read_item(item_id: int):
    """
    `response_model_exclude_unset=True` tells FastAPI to exclude fields that were not
    explicitly set when creating the model instance (omitting default values from JSON).
    """
    return Item(name="Wireless Mouse", price=29.99)


# -----------------------------------------------------------------------------
# 4. Endpoints with HTTP 204 No Content (e.g. Deletion)
# -----------------------------------------------------------------------------
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """
    HTTP 204 No Content signifies successful request with no response body.
    """
    if user_id in FAKE_USER_DB:
        del FAKE_USER_DB[user_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run("05_response_models:app", host="127.0.0.1", port=8000, reload=True)
