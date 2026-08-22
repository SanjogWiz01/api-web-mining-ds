"""
FastAPI Application Entry Point — Task Manager API.

Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routers import auth, users, tasks

# Create the FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "A production-ready Task Manager REST API built with FastAPI. "
        "Features JWT authentication, full CRUD operations, and SQLite persistence."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------- CORS Middleware ----------
# Allow all origins in development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Register Routers ----------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


# ---------- Startup Event ----------
@app.on_event("startup")
def on_startup():
    """Create database tables on application startup."""
    create_tables()


# ---------- Root Endpoint ----------
@app.get("/", tags=["Root"])
def root():
    """Health check / welcome endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Application health check."""
    return {"status": "healthy", "app": settings.APP_NAME}
