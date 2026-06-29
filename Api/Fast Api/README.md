# FastAPI Learning Guide

FastAPI is a modern, fast web framework for building APIs with Python 3.7+. It's built on Starlette (for web) and Pydantic (for data validation).

## Installation

```bash
# Install FastAPI
pip install fastapi

# Install Uvicorn (ASGI server to run FastAPI)
pip install uvicorn

# Optional but recommended
pip install python-multipart  # For form data handling
```

## Quick Start

### 1. Create and Run Your First App

```bash
# Run the main.py file
uvicorn main:app --reload

# The app will be available at: http://127.0.0.1:8000
# Interactive API docs: http://127.0.0.1:8000/docs
# Alternative docs: http://127.0.0.1:8000/redoc
```

The `--reload` flag auto-restarts the server when you change code (development only).

## Key Concepts

### Path Parameters
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```
Access: `http://127.0.0.1:8000/items/42`

### Query Parameters
```python
@app.get("/search")
def search(q: str, skip: int = 0, limit: int = 10):
    return {"query": q, "skip": skip, "limit": limit}
```
Access: `http://127.0.0.1:8000/search?q=python&skip=0&limit=5`

### Request Body (POST)
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.post("/items")
def create_item(item: Item):
    return item
```

### HTTP Methods
- `GET` - Retrieve data
- `POST` - Create data
- `PUT` - Update entire resource
- `DELETE` - Delete data
- `PATCH` - Partial update

## File Structure (Recommended)

```
fastapi-project/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── app/
│   ├── __init__.py
│   ├── models.py        # Pydantic models
│   ├── schemas.py       # Request/response schemas
│   └── routes/
│       ├── __init__.py
│       └── items.py     # Item routes
└── tests/
    └── test_main.py
```

## Pydantic Models

FastAPI uses Pydantic for automatic validation and documentation:

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

Features:
- Automatic validation
- Serialization/deserialization
- JSON schema generation
- IDE support with autocomplete

## Testing with curl

```bash
# GET request
curl http://127.0.0.1:8000/

# POST request with JSON
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":999.99,"description":"A great laptop"}'

# Query parameters
curl "http://127.0.0.1:8000/search?q=python&limit=5"
```

## Useful Features

### Dependency Injection
```python
async def get_query(q: str = None):
    return q

@app.get("/")
def read_root(query: str = Depends(get_query)):
    return {"query": query}
```

### Async Support
```python
@app.get("/async")
async def async_endpoint():
    # Can use async operations here
    return {"message": "async response"}
```

### Status Codes
```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item
```

### Error Handling
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

## Documentation

FastAPI auto-generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These are interactive and auto-updated based on your code!

## Running with Different Servers

```bash
# Development (with auto-reload)
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Specify IP and port
uvicorn main:app --host 192.168.1.100 --port 8080
```

## Next Steps

1. Explore the interactive docs at `/docs`
2. Create models for your data
3. Build routes for CRUD operations
4. Add error handling
5. Learn about middleware
6. Add authentication/security
7. Deploy to a cloud platform

## Useful Resources

- **Official Docs**: https://fastapi.tiangolo.com/
- **GitHub**: https://github.com/tiangolo/fastapi
- **Video Tutorials**: Search "FastAPI tutorial" on YouTube

## Common Errors & Solutions

**"ModuleNotFoundError: No module named 'fastapi'"**
- Solution: Run `pip install fastapi uvicorn`

**"Port 8000 already in use"**
- Solution: Use `uvicorn main:app --port 8001` or kill the process using the port

**"No module named 'uvicorn'"**
- Solution: Run `pip install uvicorn`

---

Happy coding! Start with main.py and expand from there.
