# FastAPI – Complete Learning Guide

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.

**Key features:** automatic interactive docs, request validation, async support, dependency injection, OpenAPI compliance.

---

## Table of Contents

1. [Installation & Setup](#1-installation--setup)
2. [Your First App](#2-your-first-app)
3. [Path & Query Parameters](#3-path--query-parameters)
4. [Request Body & Pydantic Models](#4-request-body--pydantic-models)
5. [Validation with Pydantic](#5-validation-with-pydantic)
6. [CRUD Operations](#6-crud-operations)
7. [Response Models](#7-response-models)
8. [Error Handling](#8-error-handling)
9. [Dependency Injection](#9-dependency-injection)
10. [Async Handlers](#10-async-handlers)
11. [Background Tasks](#11-background-tasks)
12. [Middleware & CORS](#12-middleware--cors)
13. [Authentication & Security](#13-authentication--security)
14. [File Uploads](#14-file-uploads)
15. [Database Integration (SQLAlchemy)](#15-database-integration-sqlalchemy)
16. [Testing](#16-testing)
17. [Project Structure](#17-project-structure)
18. [Deployment](#18-deployment)
19. [Best Practices](#19-best-practices)

---

## 1. Installation & Setup

```bash
pip install fastapi uvicorn
```

Optional but recommended:
```bash
pip install python-multipart   # form data / file uploads
pip install pydantic[email]    # email validation
pip install sqlalchemy         # database
pip install httpx              # TestClient
```

---

## 2. Your First App

Create `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
```

Run it:
```bash
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger docs.

---

## 3. Path & Query Parameters

### Path Parameters
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):          # type hint → automatic validation
    return {"item_id": item_id}
```
`GET /items/42` → `{"item_id": 42}`

### Query Parameters
```python
@app.get("/search")
def search(q: str, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}
```
`GET /search?q=fastapi&skip=0&limit=5`

### Optional Query Params
```python
from typing import Optional

@app.get("/items")
def list_items(category: Optional[str] = None):
    ...
```

### Advanced Validation with `Query` & `Path`
```python
from fastapi import Query, Path

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., ge=1),               # ≥ 1
    q: str = Query(None, min_length=2, max_length=50),
    page: int = Query(1, ge=1),
):
    ...
```

---

## 4. Request Body & Pydantic Models

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items")
def create_item(item: Item):
    return item
```

FastAPI automatically:
- Reads the JSON body
- Validates types
- Returns a 422 error on invalid data
- Generates JSON Schema for docs

---

## 5. Validation with Pydantic

### Field Constraints
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=100000)
    rating: int = Field(0, ge=0, le=5)
    email: str | None = Field(None, pattern=r"^\S+@\S+\.\S+$")
```

### Custom Validators
```python
from pydantic import BaseModel, field_validator

class Item(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip()
```

### Enums
```python
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(BaseModel):
    title: str
    priority: Priority
```

### Nested Models
```python
class Tag(BaseModel):
    name: str
    color: str = "blue"

class Task(BaseModel):
    title: str
    tags: list[Tag] = []
```

---

## 6. CRUD Operations

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

items = {}

@app.get("/items")
def list_items():
    return list(items.values())

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    new_id = len(items) + 1
    items[new_id] = item.model_dump()
    return {"id": new_id, **items[new_id]}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404)
    items[item_id] = item.model_dump()
    return items[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404)
    items.pop(item_id)
    return {"message": "Deleted"}
```

---

## 7. Response Models

```python
from pydantic import BaseModel
from datetime import datetime

class TaskOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    done: bool

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn):
    ...
    return record   # validated against TaskOut
```

Use `response_model_exclude_unset=True` to omit unset fields.

---

## 8. Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# Basic
raise HTTPException(status_code=404, detail="Item not found")

# Custom headers
raise HTTPException(status_code=403, detail="Forbidden", headers={"X-Error": "no access"})

# Custom exception handler
from fastapi import Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something"},
    )
```

---

## 9. Dependency Injection

```python
from fastapi import Depends

# Simple dependency
def common_params(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items")
def read_items(params: dict = Depends(common_params)):
    return params

# Class dependency
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/users")
def get_users(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

---

## 10. Async Handlers

```python
import asyncio

@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(1)
    return {"message": "async done"}

# Parallel async execution
@app.get("/parallel")
async def parallel():
    results = await asyncio.gather(
        fetch_data("source1"),
        fetch_data("source2"),
    )
    return results
```

---

## 11. Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Email sent to {email}")
    return {"message": "Notification sent"}
```

---

## 12. Middleware & CORS

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response
```

---

## 13. Authentication & Security

### Simple Token Auth
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/protected")
def protected(user: str = Depends(verify_token)):
    return {"message": "Access granted"}
```

### OAuth2 Password Flow
```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # verify form_data.username, form_data.password
    return {"access_token": "fake-token", "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

---

## 14. File Uploads

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()          # bytes
    return {
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type,
    }

# Multiple files
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return [{"filename": f.filename, "size": len(await f.read())} for f in files]
```

---

## 15. Database Integration (SQLAlchemy)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()
```

---

## 16. Testing

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_create_item():
    response = client.post("/items", json={"name": "Test", "price": 10.0})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
```

Run with:
```bash
pytest test_main.py -v
```

---

## 17. Project Structure

```
project/
├── main.py                  # entry point
├── app/
│   ├── __init__.py
│   ├── config.py            # settings
│   ├── database.py          # DB engine/session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── dependencies.py      # shared dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_items.py
│   └── test_users.py
└── requirements.txt
```

### Using `APIRouter`

```python
# app/routers/items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def list_items():
    return [{"name": "Item 1"}]

# main.py
from app.routers import items
app.include_router(items.router)
```

---

## 18. Deployment

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn (Unix only)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 19. Best Practices

| Topic | Guideline |
|-------|-----------|
| **Type hints** | Always use them everywhere |
| **Pydantic v2** | Use `model_dump()` not `dict()`; `field_validator` not `validator` |
| **Routers** | Split endpoints into `APIRouter` modules |
| **Dependencies** | Factor out auth, DB sessions, pagination |
| **Async** | Use only when doing I/O (DB, HTTP, file) |
| **Status codes** | Use `fastapi.status` constants |
| **Response models** | Always define a `response_model` for endpoints |
| **Environment** | Use `pydantic-settings` for config |
| **Testing** | Write tests with `TestClient` |
| **Security** | Never hardcode secrets; use env vars |

---

## Quick Reference – Common CLI Commands

```bash
uvicorn main:app --reload                                  # run dev server
uvicorn main:app --host 0.0.0.0 --port 8080                # custom host/port
uvicorn main:app --workers 4                               # prod with 4 workers
pytest test_main.py -v                                     # run tests
```

---

## What's Next?

1. Run `uvicorn main:app --reload` and open `/docs`
2. Work through `01_basics.py` → `02_models_validation.py` → `03_async_dependencies.py`
3. Integrate a real database (SQLAlchemy)
4. Add authentication (JWT)
5. Write tests
6. Deploy

**Official docs:** https://fastapi.tiangolo.com/
