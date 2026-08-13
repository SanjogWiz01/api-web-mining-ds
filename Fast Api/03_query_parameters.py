"""
===============================================================================
Lesson 03: Query Parameters, Defaults & Query(...) Validation
===============================================================================
80/20 Principle Focus:
- How FastAPI distinguishes Path parameters from Query parameters
- Providing default values for query parameters (`limit: int = 10`)
- Making query parameters optional (`q: str | None = None`)
- Filtering and Pagination patterns (`skip` and `limit`)
- Validation using `Query()` (min/max length, regex, list of query parameters)

How to Run:
   python 03_query_parameters.py
Test URLs:
- Defaults:    http://127.0.0.1:8000/products/
- Pagination:  http://127.0.0.1:8000/products/?skip=2&limit=3
- Filtering:   http://127.0.0.1:8000/products/search?q=phone&category=electronics
- Query List:  http://127.0.0.1:8000/tags/?tag=python&tag=fastapi&tag=api
===============================================================================
"""

from typing import Optional
from fastapi import FastAPI, Query, Path
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 03: Query Parameters",
    description="Mastering query string handling, pagination, optional inputs, and Query(...) validation.",
    version="1.0.0",
)

# Fake dataset for demonstration
FAKE_ITEMS_DB = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "electronics"},
    {"id": 2, "name": "Smartphone", "price": 699.99, "category": "electronics"},
    {"id": 3, "name": "Desk Chair", "price": 149.50, "category": "furniture"},
    {"id": 4, "name": "Coffee Mug", "price": 12.99, "category": "kitchen"},
    {"id": 5, "name": "Wireless Headphones", "price": 199.99, "category": "electronics"},
    {"id": 6, "name": "Mechanical Keyboard", "price": 89.00, "category": "electronics"},
]


# -----------------------------------------------------------------------------
# 1. Default & Optional Query Parameters (Pagination Pattern)
# -----------------------------------------------------------------------------
@app.get("/products/")
def list_products(skip: int = 0, limit: int = 5, in_stock_only: bool = False):
    """
    Function arguments NOT declared in URL path automatically become Query parameters!
    - URL example: `/products/?skip=2&limit=3&in_stock_only=true`
    - FastAPI automatically converts string boolean ("true", "1", "yes") to Python `True`!
    """
    sliced_items = FAKE_ITEMS_DB[skip : skip + limit]
    return {
        "skip": skip,
        "limit": limit,
        "in_stock_only": in_stock_only,
        "total_returned": len(sliced_items),
        "data": sliced_items,
    }


# -----------------------------------------------------------------------------
# 2. Advanced Query Validation with Query(...)
# -----------------------------------------------------------------------------
@app.get("/products/search")
def search_products(
    q: str = Query(
        ...,  # Required parameter
        min_length=3,
        max_length=50,
        description="Search term (3 to 50 characters)",
        examples=["laptop"],
    ),
    category: str | None = Query(
        default=None,
        max_length=20,
        description="Optional category filter",
    ),
):
    """
    `Query(...)` adds strict constraints to query parameters.
    Try requesting `/products/search?q=a` to trigger a min_length validation error!
    """
    results = [item for item in FAKE_ITEMS_DB if q.lower() in item["name"].lower()]

    if category:
        results = [item for item in results if item["category"].lower() == category.lower()]

    return {"query": q, "category_filter": category, "count": len(results), "results": results}


# -----------------------------------------------------------------------------
# 3. Accepting Multiple Query Parameters (List of values)
# -----------------------------------------------------------------------------
@app.get("/tags/")
def filter_by_tags(
    tag: list[str] = Query(
        default=["python"],
        description="Pass multiple tags like ?tag=python&tag=fastapi",
    )
):
    """
    To receive multiple values for the same query parameter, declare it as a list!
    URL: `/tags/?tag=python&tag=fastapi&tag=web`
    """
    return {"selected_tags": tag, "tag_count": len(tag)}


# -----------------------------------------------------------------------------
# 4. Combining Path and Query Parameters
# -----------------------------------------------------------------------------
@app.get("/users/{user_id}/orders/{order_id}")
def get_user_order(
    user_id: int = Path(..., gt=0),
    order_id: int = Path(..., gt=0),
    details: bool = Query(False, description="Include full itemized invoice details"),
):
    """
    FastAPI seamlessly parses path params (`user_id`, `order_id`) AND query params (`details`).
    URL: `/users/10/orders/500?details=true`
    """
    return {
        "user_id": user_id,
        "order_id": order_id,
        "show_details": details,
        "order_status": "Shipped",
    }


if __name__ == "__main__":
    uvicorn.run("03_query_parameters:app", host="127.0.0.1", port=8000, reload=True)
