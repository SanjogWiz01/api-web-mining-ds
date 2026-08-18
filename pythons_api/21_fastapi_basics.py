"""Real implementation: FastAPI basics.

FastAPI builds on Pydantic and Starlette:
  - automatic validation of request/response models
  - automatic OpenAPI docs at /docs and /redoc
  - async support out of the box

Run:
    pip install fastapi "uvicorn[standard]"
    python 21_fastapi_basics.py
Then open http://127.0.0.1:8000/docs
"""

from datetime import date

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI Basics", version="0.1.0")


# ------------------------------------------------------------------- models
class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=80)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    birthday: date | None = None


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ------------------------------------------------------------------ endpoints
@app.get("/")
def root():
    return {"message": "hello from FastAPI", "docs": "/docs"}


@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(gt=0, description="The item id"),
    verbose: bool = Query(False, description="Include extra detail"),
):
    """Path + query params with validation."""
    item = {"id": item_id, "name": f"item-{item_id}"}
    if verbose:
        item["verbose"] = True
    return item


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    """Request body is validated by Pydantic automatically."""
    return User(id=42, **user.model_dump())


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 42:
        raise HTTPException(status_code=404, detail="User not found")
    return User(id=42, name="Sanjog", email="sanjo@example.com")


@app.get("/math/add")
def add(a: int = Query(ge=-1000, le=1000), b: int = Query(ge=-1000, le=1000)):
    return {"result": a + b}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
