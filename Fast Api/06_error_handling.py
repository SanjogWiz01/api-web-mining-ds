"""
===============================================================================
Lesson 06: Error Handling & Custom Exceptions
===============================================================================
80/20 Principle Focus:
- Raising standard `HTTPException` with proper status codes & headers
- Custom error detail messages and dictionaries
- Writing custom Exception classes
- Global `@app.exception_handler` decorators for consistent API error schemas

How to Run:
   python 06_error_handling.py
Test URLs:
- Found item:     http://127.0.0.1:8000/items/1
- Not found:      http://127.0.0.1:8000/items/999  (Returns clean HTTP 404 JSON)
- Custom exception: http://127.0.0.1:8000/custom-error/foo
===============================================================================
"""

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 06: Error Handling",
    description="Learn robust exception handling and custom error responses in FastAPI.",
    version="1.0.0",
)

ITEMS_DB = {
    1: {"name": "Mechanical Keyboard", "stock": 15},
    2: {"name": "Gaming Mouse", "stock": 0},
}


# -----------------------------------------------------------------------------
# 1. Raising Standard HTTPException
# -----------------------------------------------------------------------------
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    If item doesn't exist, raise HTTPException(status_code=404).
    FastAPI handles translating Python exceptions into JSON HTTP responses!
    """
    if item_id not in ITEMS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} does not exist in inventory.",
        )
    return ITEMS_DB[item_id]


# -----------------------------------------------------------------------------
# 2. Raising HTTPException with Custom Headers & Structured Detail
# -----------------------------------------------------------------------------
@app.post("/items/{item_id}/purchase")
def purchase_item(item_id: int, quantity: int = 1):
    """
    Handling domain errors (out of stock) with headers and structured dict details.
    """
    if item_id not in ITEMS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "ITEM_NOT_FOUND", "item_id": item_id},
        )

    item = ITEMS_DB[item_id]
    if item["stock"] < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "INSUFFICIENT_STOCK",
                "requested": quantity,
                "available": item["stock"],
            },
            headers={"X-Error-Reason": "StockDepleted"},
        )

    item["stock"] -= quantity
    return {"message": "Purchase successful", "remaining_stock": item["stock"]}


# -----------------------------------------------------------------------------
# 3. Defining & Handling Custom Domain Exceptions
# -----------------------------------------------------------------------------
# Step A: Custom Python Exception class
class InvalidLicenseKeyException(Exception):
    def __init__(self, key: str):
        self.key = key


# Step B: Register an exception handler for this exception class
@app.exception_handler(InvalidLicenseKeyException)
def invalid_license_handler(request: Request, exc: InvalidLicenseKeyException):
    """
    Whenever `InvalidLicenseKeyException` is raised anywhere in the code,
    this custom handler intercepts it and formats a standard JSON response.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "status": "error",
            "message": f"License key '{exc.key}' is invalid or expired.",
            "help": "Please contact support@example.com to renew your subscription.",
            "path": request.url.path,
        },
    )


@app.get("/verify-license/{key}")
def verify_license(key: str):
    """Endpoint that triggers custom exception if key is not 'VALID-123'."""
    if key != "VALID-123":
        raise InvalidLicenseKeyException(key=key)
    return {"status": "success", "license": key, "active": True}


if __name__ == "__main__":
    uvicorn.run("06_error_handling:app", host="127.0.0.1", port=8000, reload=True)
