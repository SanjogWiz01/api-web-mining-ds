"""
===============================================================================
Lesson 10: Async Operations, Background Tasks & Middleware
===============================================================================
80/20 Principle Focus:
- `async def` vs synchronous `def` (when and why to use async)
- Non-blocking Background Tasks (`BackgroundTasks`) for sending emails / logging
- Writing HTTP Middleware (e.g. process timing headers `X-Process-Time`)
- SQLite database interaction pattern (creating tables & inserting rows dynamically)
- Summary recap of the FastAPI 80/20 mastery path!

How to Run:
   python 10_async_db_and_background_tasks.py
Test URLs:
- Async Endpoint:   http://127.0.0.1:8000/async-data
- Background Task:  POST http://127.0.0.1:8000/send-notification/ (Check terminal output!)
- SQLite Users:     http://127.0.0.1:8000/db/users/
===============================================================================
"""

import asyncio
import sqlite3
import time
from fastapi import FastAPI, BackgroundTasks, Request, status
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 10: Async & Background Tasks",
    description="Mastering asynchronous execution, non-blocking background workers, and middleware.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 1. Custom HTTP Middleware (Execution Timing)
# -----------------------------------------------------------------------------
@app.middleware("http")
def add_process_time_header(request: Request, call_next):
    """
    Middleware runs before AND after every request.
    Measures processing duration and adds `X-Process-Time` header to response.
    """
    start_time = time.time()
    response = call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f} sec"
    return response


# -----------------------------------------------------------------------------
# 2. Async Endpoints (`async def` with await)
# -----------------------------------------------------------------------------
@app.get("/async-data")
async def get_async_data():
    """
    Use `async def` when performing non-blocking I/O operations (async DB, httpx, asyncio.sleep).
    FastAPI runs async endpoints on the main event loop for extreme performance!
    """
    print("Simulating non-blocking I/O fetching external API...")
    await asyncio.sleep(1.5)  # Simulates 1.5 second non-blocking network request
    return {
        "status": "success",
        "message": "Async data fetched without blocking other incoming requests!",
        "elapsed": "1.5s simulated delay",
    }


# -----------------------------------------------------------------------------
# 3. Background Tasks (Non-blocking response dispatch)
# -----------------------------------------------------------------------------
def write_audit_log(email: str, message: str):
    """Simulated slow background task (e.g. sending email, generating PDF, audit log)."""
    time.sleep(2)  # Simulate slow I/O
    with open("audit_notifications.log", "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Email sent to {email}: {message}\n")
    print(f"--> [BACKGROUND WORKER COMPLETE] Notification email sent to {email}")


class NotificationRequest(BaseModel):
    email: str
    message: str


@app.post("/send-notification/", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(payload: NotificationRequest, background_tasks: BackgroundTasks):
    """
    The response returns INSTANTLY with HTTP 202 Accepted.
    The `write_audit_log` function executes in the background AFTER response delivery!
    """
    # Enqueue task for background execution
    background_tasks.add_task(write_audit_log, email=payload.email, message=payload.message)

    return {
        "message": "Notification scheduled for background processing.",
        "recipient": payload.email,
        "status": "queued",
    }


# -----------------------------------------------------------------------------
# 4. SQLite Database Pattern
# -----------------------------------------------------------------------------
DB_FILE = "fastapi_demo.db"


def init_sqlite_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


init_sqlite_db()


class UserCreateSchema(BaseModel):
    name: str
    email: str


@app.post("/db/users/", status_code=status.HTTP_201_CREATED)
def create_db_user(user: UserCreateSchema):
    """Insert user record into SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "name": user.name, "email": user.email}
    except sqlite3.IntegrityError:
        return {"error": "User with this email already exists."}
    finally:
        conn.close()


@app.get("/db/users/")
def list_db_users():
    """Query user records from SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]


if __name__ == "__main__":
    print("=================================================================")
    print("FastAPI 80/20 Mastery Course Complete!")
    print("Run `python 10_async_db_and_background_tasks.py` to launch.")
    print("=================================================================")
    uvicorn.run("10_async_db_and_background_tasks:app", host="127.0.0.1", port=8000, reload=True)
