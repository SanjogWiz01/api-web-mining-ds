"""
===============================================================================
Lesson 01: First Steps with FastAPI
===============================================================================
80/20 Principle Focus:
- Creating a FastAPI application instance (`FastAPI()`)
- Defining HTTP GET endpoints using operation decorators (`@app.get`)
- Automatic JSON response serialization (dicts, lists, primitives)
- Free interactive API documentation at `/docs` (Swagger) and `/redoc` (ReDoc)

How to Run:
1. Terminal command:
   uvicorn 01_first_steps:app --reload
2. Or run directly with Python:
   python 01_first_steps.py

Interactive Docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc:      http://127.0.0.1:8000/redoc
===============================================================================
"""

from fastapi import FastAPI
import uvicorn

# 1. Create the main FastAPI instance
# Title, description, and version automatically customize your /docs page!
app = FastAPI(
    title="FastAPI 80/20 - Lesson 01: First Steps",
    description="Learn the absolute core basics of FastAPI endpoints and automatic OpenAPI generation.",
    version="1.0.0",
)


# 2. Define a root GET route
# The decorator @app.get("/") tells FastAPI that the function below handles GET requests to "/"
@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome JSON payload.
    Docstrings inside endpoint functions appear directly in OpenAPI /docs!
    """
    return {
        "message": "Welcome to FastAPI!",
        "status": "online",
        "docs_url": "http://127.0.0.1:8000/docs",
    }


# 3. Define another GET route for health checks
@app.get("/health")
def health_check():
    """Simple health monitoring endpoint."""
    return {"status": "healthy", "service": "learning-fastapi"}


# 4. Define a route returning a list of dictionary items
@app.get("/info")
def get_info():
    """FastAPI automatically converts Python dicts, lists, integers, strings to JSON."""
    return {
        "framework": "FastAPI",
        "language": "Python 3.10+",
        "key_features": [
            "Automatic OpenAPI / Swagger UI docs",
            "High performance powered by Starlette and Pydantic",
            "Python type hint data validation",
        ],
    }


# Direct execution block so you can start the server by simply running: `python 01_first_steps.py`
if __name__ == "__main__":
    uvicorn.run("01_first_steps:app", host="127.0.0.1", port=8000, reload=True)
