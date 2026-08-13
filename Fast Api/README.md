# FastAPI 80/20 Mastery Course

Welcome to the **FastAPI 80/20 Learning Guide**!

The **80/20 Principle (Pareto Principle)** states that 80% of real-world results come from 20% of core concepts. This course focuses on the exact 20% of FastAPI features that you will use in almost every production API project.

---

## 🚀 Quick Start

### 1. Install Dependencies
Make sure you have FastAPI and Uvicorn installed:
```powershell
pip install -r requirements.txt
```

### 2. Running Any Lesson
Every script is self-contained and runnable! You can start any lesson using standard Python:
```powershell
python 01_first_steps.py
```
Or directly with `uvicorn`:
```powershell
uvicorn 01_first_steps:app --reload
```

### 3. Interactive API Documentation
Once a server is running, open your web browser to test endpoints interactively:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI**:   [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 Curriculum Roadmap (10 Lessons)

| Lesson File | Core 80/20 Concept | Key Takeaway |
| :--- | :--- | :--- |
| **`01_first_steps.py`** | FastAPI Instance & Endpoints | Setting up `FastAPI()`, route decorators (`@app.get`), automatic JSON serialization & free `/docs`. |
| **`02_path_parameters.py`** | Path Variables & Type Safety | Dynamic parameters in URLs (`/users/{id}`), Enums, type casting, path validation (`Path`). |
| **`03_query_parameters.py`** | Query String & Validation | Optional parameters, default values, pagination (`skip`, `limit`), validation with `Query()`. |
| **`04_request_body_pydantic.py`** | Request Body & Pydantic | Defining JSON schemas using Pydantic `BaseModel`, `Field(...)` validation rules, nested models. |
| **`05_response_models.py`** | Response Models & HTTP Status | Filtering outgoing data (`response_model`), hiding sensitive fields (passwords), HTTP status codes. |
| **`06_error_handling.py`** | Exceptions & Custom Handlers | Raising `HTTPException`, custom headers, global exception handlers with `@app.exception_handler`. |
| **`07_dependency_injection.py`** | Dependency Injection (`Depends`) | Reusable code, request pre-processing, header security checks, cleanup using `yield`. |
| **`08_crud_application.py`** | Complete REST CRUD API | Putting lessons 1-7 together: full Create, Read, Update, Delete REST application for Books. |
| **`09_routers_and_modules.py`** | Modular Architecture (`APIRouter`) | Structuring large projects with `APIRouter`, module prefixes, OpenAPI tags, sub-routers. |
| **`10_async_db_and_background_tasks.py`** | Async, Background Tasks & Middleware | `async def` vs `def`, non-blocking `BackgroundTasks`, process timing middleware, SQLite storage. |

---

## 🛠️ Summary of Key 80/20 Concepts

1. **Automatic Data Validation**: FastAPI inspects Python type hints (`int`, `str`, `float`, `bool`, Pydantic models) to parse and validate HTTP requests automatically. If data is invalid, it returns clean HTTP 422 JSON errors.
2. **Pydantic BaseModels**: Inbound JSON payloads and outbound JSON responses use Pydantic models to guarantee strict data contracts.
3. **Dependency Injection System (`Depends`)**: Avoid code repetition by injecting database sessions, authentication checks, and common query parameters cleanly into endpoint functions.
4. **Interactive OpenAPI Docs**: No manual documentation writing needed — OpenAPI / Swagger UI specs are built automatically from your function names, type hints, Pydantic models, and docstrings.
5. **Asynchronous & Synchronous Support**: Use `async def` for non-blocking I/O (network/async DB calls) and `def` for standard synchronous code.

Happy coding & learning FastAPI! 🚀
