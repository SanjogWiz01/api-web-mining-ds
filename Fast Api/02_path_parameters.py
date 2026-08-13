"""
===============================================================================
Lesson 02: Path Parameters & Type Validation
===============================================================================
80/20 Principle Focus:
- Extracting dynamic variables from URL paths (`/users/{user_id}`)
- Python type hints for automatic string-to-int/float/bool conversion
- Predefined path parameters using standard Python `Enum`
- Advanced path validation using `Path(gt=0, description=...)`
- Filepath converters (`{file_path:path}`)

How to Run:
   python 02_path_parameters.py
Test URLs:
- Valid int:    http://127.0.0.1:8000/users/42
- Invalid int:  http://127.0.0.1:8000/users/not-an-id  (Notice 422 validation error!)
- Enum test:    http://127.0.0.1:8000/models/alexnet
- Path test:    http://127.0.0.1:8000/files/logs/2026/app.log
===============================================================================
"""

from enum import Enum
from fastapi import FastAPI, Path, HTTPException, status
import uvicorn

app = FastAPI(
    title="FastAPI 80/20 - Lesson 02: Path Parameters",
    description="Mastering dynamic URL paths, type enforcement, Enums, and Path validation.",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# 1. Basic Path Parameter with Automatic Type Casting & Validation
# -----------------------------------------------------------------------------
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    FastAPI reads `user_id` from URL path and converts it to integer automatically.
    If you request `/users/foo`, FastAPI returns HTTP 422 automatically with details!
    """
    return {
        "user_id": user_id,
        "type_received": str(type(user_id)),
        "message": f"Successfully fetched user #{user_id}",
    }


# -----------------------------------------------------------------------------
# 2. Path Parameters with Predefined Values using Enum
# -----------------------------------------------------------------------------
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    """
    Using Enum restricts valid path values to a fixed list.
    Swagger UI will render a dropdown menu for `model_name`!
    """
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning Classic!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeNet for digit recognition."}

    return {"model_name": model_name, "message": "ResNet residual learning architecture."}


# -----------------------------------------------------------------------------
# 3. Path Validation using FastAPI's Path(...)
# -----------------------------------------------------------------------------
@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(
        ...,  # '...' means required parameter
        title="The ID of the item to get",
        description="Must be a positive integer greater than 0 and less than 10000",
        gt=0,     # Greater than 0
        lt=10000, # Less than 10000
    )
):
    """
    Path(...) allows adding validation constraints (gt, ge, lt, le, regex pattern).
    Try requesting /items/0 or /items/99999 to see automatic validation failure!
    """
    return {"item_id": item_id, "status": "item active"}


# -----------------------------------------------------------------------------
# 4. File Path Converter ({file_path:path})
# -----------------------------------------------------------------------------
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    """
    Using `:path` tells FastAPI to match any URL path including slashes `/`.
    Example URL: `/files/data/reports/summary.csv`
    """
    return {"file_path": file_path, "sub_directories": file_path.split("/")}


if __name__ == "__main__":
    uvicorn.run("02_path_parameters:app", host="127.0.0.1", port=8000, reload=True)
