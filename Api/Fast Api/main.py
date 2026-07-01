cfrom fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="My FastAPI App", # this is ommment 
    description="A learning project for FastAPI",
    version="1.0.0"
)

# ============================================================================
# PYDANTIC MODELS (Data validation)
# ============================================================================

class Item(BaseModel):
    """Model for Item data"""
    id: Optional[int] = None  # Optional, not required in request
    name: str  # Required
    description: Optional[str] = None  # Optional with default None
    price: float
    tax: Optional[float] = None
    is_available: bool = True
    
    # Pydantic model config
    class Config:
        example = {
            "name": "Laptop",
            "description": "A high-performance laptop",
            "price": 1299.99,
            "tax": 129.99,
            "is_available": True
        }


class User(BaseModel):
    """Model for User data"""
    username: str
    email: str
    age: Optional[int] = None
    is_active: bool = True


# ============================================================================
# IN-MEMORY DATABASE (For learning - replace with real DB later)
# ============================================================================

fake_items_db = {
    1: {"id": 1, "name": "Laptop", "price": 999.99, "description": "Dell XPS"},
    2: {"id": 2, "name": "Mouse", "price": 29.99, "description": "Wireless Mouse"},
    3: {"id": 3, "name": "Monitor", "price": 299.99, "description": "4K Monitor"},
}

fake_users_db = {
    1: {"username": "john_doe", "email": "john@example.com", "age": 25, "is_active": True},
    2: {"username": "jane_smith", "email": "jane@example.com", "age": 30, "is_active": True},
}

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
def read_root():
    """
    Root endpoint - returns welcome message
    Access: http://127.0.0.1:8000/
    """
    return {
        "message": "Welcome to FastAPI!",
        "timestamp": datetime.now(),
        "endpoints": {
            "items": "/items",
            "users": "/users",
            "docs": "/docs"
        }
    }


# ============================================================================
# ITEMS ENDPOINTS (CRUD operations)
# ============================================================================

@app.get("/items", tags=["Items"])
def get_all_items(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """
    Get all items with pagination
    
    Query parameters:
    - skip: Number of items to skip (default: 0)
    - limit: Maximum items to return (default: 10, max: 100)
    
    Example: /items?skip=0&limit=5
    """
    items = list(fake_items_db.values())
    return {
        "total": len(items),
        "skip": skip,
        "limit": limit,
        "items": items[skip : skip + limit]
    }


@app.get("/items/{item_id}", tags=["Items"])
def get_item(item_id: int):
    """
    Get a single item by ID
    
    Path parameter:
    - item_id: The ID of the item
    
    Example: /items/1
    """
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return fake_items_db[item_id]


@app.post("/items", tags=["Items"], status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    """
    Create a new item
    
    Request body: JSON with Item fields
    
    Example:
    {
        "name": "Keyboard",
        "price": 149.99,
        "description": "Mechanical Keyboard",
        "is_available": true
    }
    """
    # Generate new ID
    new_id = max(fake_items_db.keys()) + 1 if fake_items_db else 1
    item_dict = item.dict()
    item_dict["id"] = new_id
    
    fake_items_db[new_id] = item_dict
    
    return {
        "message": "Item created successfully",
        "item": item_dict
    }


@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, item: Item):
    """
    Update an entire item
    
    Path parameter:
    - item_id: The ID of the item to update
    
    Request body: Complete Item data
    """
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    item_dict = item.dict()
    item_dict["id"] = item_id
    fake_items_db[item_id] = item_dict
    
    return {
        "message": "Item updated successfully",
        "item": item_dict
    }


@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    """
    Delete an item
    
    Path parameter:
    - item_id: The ID of the item to delete
    """
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    deleted_item = fake_items_db.pop(item_id)
    return {
        "message": "Item deleted successfully",
        "deleted_item": deleted_item
    }


# ============================================================================
# SEARCH ENDPOINT (Query parameters)
# ============================================================================

@app.get("/items/search/by-name", tags=["Items"])
def search_items(q: str = Query(..., min_length=1, max_length=50)):
    """
    Search items by name
    
    Query parameter:
    - q: Search query (required)
    
    Example: /items/search/by-name?q=laptop
    """
    results = [
        item for item in fake_items_db.values()
        if q.lower() in item["name"].lower()
    ]
    
    return {
        "query": q,
        "total_results": len(results),
        "items": results
    }


# ============================================================================
# USERS ENDPOINTS
# ============================================================================

@app.get("/users", tags=["Users"])
def get_users():
    """Get all users"""
    return {
        "total": len(fake_users_db),
        "users": list(fake_users_db.values())
    }


@app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return fake_users_db[user_id]


@app.post("/users", tags=["Users"], status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    """Create a new user"""
    new_id = max(fake_users_db.keys()) + 1 if fake_users_db else 1
    user_dict = user.dict()
    fake_users_db[new_id] = user_dict
    
    return {
        "message": "User created successfully",
        "user_id": new_id,
        "user": user_dict
    }


# ============================================================================
# ADVANCED ENDPOINTS
# ============================================================================

@app.get("/items/{item_id}/details", tags=["Items"])
def get_item_details(
    item_id: int,
    include_tax: bool = Query(False),
    currency: str = Query("USD")
):
    """
    Get item details with optional tax and currency
    
    Query parameters:
    - include_tax: Include tax in calculation (boolean)
    - currency: Currency type (default: USD)
    
    Example: /items/1/details?include_tax=true&currency=USD
    """
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    item = fake_items_db[item_id].copy()
    
    if include_tax and item.get("tax"):
        item["total_price"] = item["price"] + item["tax"]
    else:
        item["total_price"] = item["price"]
    
    item["currency"] = currency
    return item


@app.post("/items/bulk-create", tags=["Items"])
def create_multiple_items(items: List[Item]):
    """
    Create multiple items at once
    
    Request body: Array of Item objects
    """
    created_items = []
    
    for item in items:
        new_id = max(fake_items_db.keys()) + 1 if fake_items_db else 1
        item_dict = item.dict()
        item_dict["id"] = new_id
        fake_items_db[new_id] = item_dict
        created_items.append(item_dict)
    
    return {
        "message": f"{len(created_items)} items created",
        "items": created_items
    }


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint
    
    Returns: Status of the API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }


# ============================================================================
# If you want to run this file directly:
# python main.py
# Then access: http://127.0.0.1:8000
#
# Or run with Uvicorn:
# uvicorn main:app --reload
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
