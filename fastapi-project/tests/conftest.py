"""
Shared test fixtures for the FastAPI test suite.
Uses an in-memory SQLite database to isolate tests from production data.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# In-memory SQLite for fast, isolated tests
TEST_DATABASE_URL = "sqlite:///./test_task_manager.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Yield a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the database dependency with our test database
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create all tables before each test, drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Provide a TestClient instance for making API requests."""
    return TestClient(app)


@pytest.fixture
def authenticated_client(client):
    """
    Register a test user, login, and return a client
    with the Authorization header pre-set.
    """
    # Register
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
    })

    # Login
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass123",
    })
    token = response.json()["access_token"]

    # Set auth header
    client.headers["Authorization"] = f"Bearer {token}"
    return client
