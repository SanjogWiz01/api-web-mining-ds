"""
===============================================================================
Lesson 04: Request Body & Pydantic Data Validation
===============================================================================
80/20 Principle Focus:
- Defining JSON schemas using Pydantic `BaseModel`
- POST endpoint handling (`@app.post`)
- Data validation rules with Pydantic `Field(...)`
- Nested models (complex JSON structures)
- Automatic request body parsing & error responses

How to Run:
   python 04_request_body_pydantic.py
Interactive Docs Test:
- Open http://127.0.0.1:8000/docs
- Test the POST `/items/` endpoint with custom JSON bodies!
===============================================================================
"""

from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, Field, HttpUrl
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 04: Request Bodies & Pydantic",
    description="Learn to validate incoming JSON bodies cleanly with Pydantic BaseModels.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 1. Sub-model for Nested JSON Structure
# -----------------------------------------------------------------------------
class Image(BaseModel):
    url: str = Field(..., description="Image URL", example="https://example.com/cover.jpg")
    name: str = Field(..., description="Image caption or title", example="Main Product View")


# -----------------------------------------------------------------------------
# 2. Main Pydantic Schema with Field Validations
# -----------------------------------------------------------------------------
class ItemCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name of the item",
        example="Wireless Headphones",
    )
    description: str | None = Field(
        default=None,
        max_length=300,
        description="Optional detailed description",
        example="Noise-canceling over-ear bluetooth headphones",
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price must be strictly positive (greater than 0)",
        example=199.99,
    )
    tax: float | None = Field(
        default=None,
        ge=0,
        description="Optional tax amount",
        example=15.50,
    )
    tags: list[str] = Field(
        default_factory=list,
        description="List of associated tags",
        example=["audio", "electronics", "sale"],
    )
    images: list[Image] | None = Field(
        default=None,
        description="Optional list of nested image objects",
    )


# -----------------------------------------------------------------------------
# 3. Endpoint Accepting Request Body
# -----------------------------------------------------------------------------
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """
    FastAPI receives the JSON body, converts it to an instance of `ItemCreate`,
    and validates all fields before execution reaching this function!

    If price is <= 0 or name is missing, FastAPI aborts with 422 Unprocessable Entity!
    """
    # Calculate price with tax if tax is supplied
    total_price = item.price
    if item.tax is not None:
        total_price += item.tax

    # Pydantic models convert cleanly back to Python dict via .model_dump()
    item_dict = item.model_dump()
    item_dict["total_calculated_price"] = round(total_price, 2)

    return {
        "message": "Item successfully created",
        "item_data": item_dict,
    }


# -----------------------------------------------------------------------------
# 4. Combining Request Body + Path + Query Parameters
# -----------------------------------------------------------------------------
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate, notify: bool = False):
    """
    FastAPI seamlessly distinguishes:
    - Path parameter: `item_id` (from URL path)
    - Body payload:   `item` (from JSON body)
    - Query parameter: `notify` (from query string)
    """
    return {
        "item_id": item_id,
        "updated_item": item,
        "notification_sent": notify,
    }


if __name__ == "__main__":
    uvicorn.run("04_request_body_pydantic:app", host="127.0.0.1", port=8000, reload=True)
