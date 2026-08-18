"""Real implementation: FastAPI CRUD API with validation and docs.

Same endpoints as the Flask version (20_flask_crud.py) but with:
  - Pydantic request/response models
  - typed responses and errors
  - automatic OpenAPI documentation

Run:
    pip install fastapi "uvicorn[standard]"
    python 22_fastapi_crud.py
Then open http://127.0.0.1:8000/docs
"""

import time
import uuid
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="Items CRUD", version="1.0.0")


# ------------------------------------------------------------------- models
class Item(BaseModel):
    id: str
    name: str
    created_at: float


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class ItemUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class ItemsPage(BaseModel):
    data: list[Item]
    meta: dict[str, int | None]


# --------------------------------------------------------------------- store
_store: dict[str, dict] = {}


def _get_or_404(item_id: str) -> dict:
    item = _store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ----------------------------------------------------------------- endpoints
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items", response_model=ItemsPage)
def list_items(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    all_items = list(_store.values())
    start = (page - 1) * limit
    return ItemsPage(
        data=[Item(**i) for i in all_items[start:start + limit]],
        meta={"page": page, "limit": limit, "total": len(all_items)},
    )


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str):
    return Item(**_get_or_404(item_id))


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate):
    now = time.time()
    item = {"id": uuid.uuid4().hex, "name": payload.name.strip(), "created_at": now}
    _store[item["id"]] = item
    return Item(**item)


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, payload: ItemUpdate):
    item = _get_or_404(item_id)
    item["name"] = payload.name.strip()
    return Item(**item)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str):
    _get_or_404(item_id)
    del _store[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
