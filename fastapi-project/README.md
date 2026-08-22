# FastAPI Project — Task Manager API

A production-ready **Task Manager REST API** built with **FastAPI**, featuring CRUD operations, authentication, database integration, and comprehensive documentation.

## Features

- 🚀 **FastAPI** with async support
- 🗄️ **SQLite + SQLAlchemy** for persistence
- 🔐 **JWT Authentication** (register, login, token refresh)
- 📋 **Task CRUD** — create, read, update, delete tasks
- 👤 **User management** with hashed passwords
- 📄 **Auto-generated docs** at `/docs` (Swagger) and `/redoc`
- ✅ **Pydantic v2** schemas with validation
- 🧪 **Pytest** test suite
- 📁 Clean modular project structure

## Project Structure

```
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py            # Application entry point
│   ├── config.py           # Settings & configuration
│   ├── database.py         # Database engine & session
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/            # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routers/            # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── tasks.py
│   ├── services/           # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── task.py
│   └── dependencies.py     # Shared dependencies (auth, db)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Visit docs
open http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Description            | Auth Required |
| ------ | ------------------ | ---------------------- | ------------- |
| POST   | `/auth/register`   | Register a new user    | No            |
| POST   | `/auth/login`      | Login & get JWT token  | No            |
| GET    | `/users/me`        | Get current user info  | Yes           |
| GET    | `/tasks/`          | List user's tasks      | Yes           |
| POST   | `/tasks/`          | Create a new task      | Yes           |
| GET    | `/tasks/{id}`      | Get task by ID         | Yes           |
| PUT    | `/tasks/{id}`      | Update a task          | Yes           |
| DELETE | `/tasks/{id}`      | Delete a task          | Yes           |

## License

MIT
