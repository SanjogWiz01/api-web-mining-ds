"""
===============================================================================
Lesson 07: Dependency Injection (`Depends`)
===============================================================================
80/20 Principle Focus:
- Understanding FastAPI's core power feature: `Depends(...)`
- Code reusability for request parameters, database sessions, and auth
- Sub-dependencies (chaining dependencies)
- Header validation dependencies
- Resource cleanup using dependencies with `yield`

How to Run:
   python 07_dependency_injection.py
Test URLs:
- Shared Pagination: http://127.0.0.1:8000/users/?skip=0&limit=2
- Header Security:   http://127.0.0.1:8000/protected/ (Requires Header `X-API-Key: secret-token`)
- Resource Yield:    http://127.0.0.1:8000/db-resource/
===============================================================================
"""

from typing import Annotated, Generator
from fastapi import FastAPI, Depends, HTTPException, Header, status
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 07: Dependency Injection",
    description="Learn FastAPI's powerful Dependency Injection system using `Depends`.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 1. Simple Function Dependency (Shared Pagination logic)
# -----------------------------------------------------------------------------
def common_pagination_params(skip: int = 0, limit: int = 10):
    """
    Shared dependency function. FastAPI automatically inspects its arguments,
    extracts `skip` and `limit` from query parameters, and passes the dict result!
    """
    return {"skip": skip, "limit": limit}


@app.get("/users/")
def get_users(pagination: dict = Depends(common_pagination_params)):
    """
    The `pagination` variable receives the dictionary returned by `common_pagination_params`.
    """
    return {
        "endpoint": "users",
        "pagination_applied": pagination,
        "users": ["Alice", "Bob", "Charlie"][pagination["skip"] : pagination["skip"] + pagination["limit"]],
    }


@app.get("/orders/")
def get_orders(pagination: dict = Depends(common_pagination_params)):
    """Reusing the exact same pagination dependency across multiple routes!"""
    return {
        "endpoint": "orders",
        "pagination_applied": pagination,
        "orders": [101, 102, 103, 104],
    }


# -----------------------------------------------------------------------------
# 2. Header & Authentication Dependency
# -----------------------------------------------------------------------------
def verify_api_key(x_api_key: str = Header(..., description="Secret API key in request header")):
    """
    Dependency to validate API key headers.
    FastAPI automatically converts parameter `x_api_key` to header name `X-API-Key`!
    """
    if x_api_key != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return x_api_key


@app.get("/protected/")
def get_protected_data(api_key: str = Depends(verify_api_key)):
    """
    This endpoint cannot be called without a valid `X-API-Key: secret-token` header.
    Try testing this in http://127.0.0.1:8000/docs!
    """
    return {
        "status": "authenticated",
        "secret_data": "Top secret information accessible only with valid API key.",
        "api_key_used": api_key,
    }


# -----------------------------------------------------------------------------
# 3. Class-Based Dependency
# -----------------------------------------------------------------------------
class QueryFilter:
    def __init__(self, q: str | None = None, category: str = "all"):
        self.q = q
        self.category = category


@app.get("/search/")
def search_catalog(filter_params: QueryFilter = Depends(QueryFilter)):
    """
    FastAPI can use Python classes directly as dependencies!
    `Depends(QueryFilter)` creates an instance of `QueryFilter` populated from query parameters.
    """
    return {
        "query": filter_params.q,
        "category": filter_params.category,
    }


# -----------------------------------------------------------------------------
# 4. Dependency with Yield (Setup and Cleanup pattern)
# -----------------------------------------------------------------------------
def get_db_connection() -> Generator[str, None, None]:
    """
    Dependencies with `yield` allow setup BEFORE endpoint execution,
    and cleanup AFTER the response is sent (e.g. closing database connections/files)!
    """
    # Setup step
    print("--> Connecting to simulated database...")
    db_session = "Simulated_DB_Session_Active"

    try:
        yield db_session
    finally:
        # Cleanup step (Always runs even if route throws an error!)
        print("<-- Closing database connection session.")


@app.get("/db-resource/")
def read_db_resource(db: str = Depends(get_db_connection)):
    """Route receiving db session initialized by yield dependency."""
    return {"status": "success", "db_session": db}


if __name__ == "__main__":
    uvicorn.run("07_dependency_injection:app", host="127.0.0.1", port=8000, reload=True)
