"""Real implementation: OpenAPI documentation generation.

FastAPI generates an OpenAPI 3 schema for free at /openapi.json and serves
Swagger UI at /docs plus ReDoc at /redoc. This file:
  1. builds a small but complete API,
  2. shows how to enrich the OpenAPI schema (metadata, tags, examples),
  3. exports the schema to disk.

Run:
    pip install fastapi "uvicorn[standard]"
    python 28_openapi_docs.py
Then open http://127.0.0.1:8000/docs and /redoc, and ./openapi.json appears.
"""

import json
from typing import Annotated, Literal

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

DESCRIPTION = """
This API demonstrates **production documentation**:

- Every endpoint is typed (request/response models).
- Tags group related endpoints in the docs.
- Examples show exactly how to call each endpoint.
- Security schemes document the auth requirement.

The OpenAPI schema is exposed at `/openapi.json` and exported to `openapi.json`.
"""

app = FastAPI(
    title="Documented Store API",
    version="2.0.0",
    description=DESCRIPTION,
    contact={"name": "Sanjog", "url": "https://github.com/SanjogWiz01"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "products", "description": "Read and manage products"},
        {"name": "system", "description": "Health and metadata"},
    ],
)


# ------------------------------------------------------------------- models
class Product(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0, description="Price in USD")
    currency: Literal["USD", "EUR"] = "USD"
    in_stock: bool = True


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80, examples=["Wireless mouse"])
    price: float = Field(gt=0, examples=[24.99])
    currency: Literal["USD", "EUR"] = "USD"
    in_stock: bool = True


_store: dict[int, Product] = {
    1: Product(id=1, name="Keyboard", price=49.99),
    2: Product(id=2, name="Monitor", price=199.99),
}
_next_id = 3


# ----------------------------------------------------------------- endpoints
@app.get("/health", tags=["system"], summary="Liveness check")
def health():
    return {"status": "ok"}


@app.get(
    "/products",
    tags=["products"],
    summary="List products",
    description="Paginated product list, sorted by id.",
)
def list_products(
    page: Annotated[int, Query(ge=1, description="Page number", examples=[1])] = 1,
    limit: Annotated[int, Query(ge=1, le=50, description="Items per page")] = 10,
):
    items = sorted(_store.values(), key=lambda p: p.id)
    start = (page - 1) * limit
    return {
        "data": [p.model_dump() for p in items[start:start + limit]],
        "meta": {"page": page, "limit": limit, "total": len(items)},
    }


@app.get("/products/{product_id}", tags=["products"], summary="Get one product")
def get_product(product_id: int):
    product = _store.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", tags=["products"], summary="Create product", status_code=201)
def create_product(payload: ProductCreate):
    global _next_id
    product = Product(id=_next_id, **payload.model_dump())
    _next_id += 1
    _store[product.id] = product
    return product


@app.delete("/products/{product_id}", tags=["products"], summary="Delete product", status_code=204)
def delete_product(product_id: int):
    if product_id not in _store:
        raise HTTPException(status_code=404, detail="Product not found")
    del _store[product_id]
    return None


# ------------------------------------------------------------- documentation
@app.get("/openapi/export")
def export_openapi(x_api_key: Annotated[str | None, Header()] = None):
    """Export the generated OpenAPI schema to a file on disk."""
    if x_api_key != "admin-secret":
        raise HTTPException(status_code=401, detail="admin-secret header required")
    schema = app.openapi()
    with open("openapi.json", "w") as f:
        json.dump(schema, f, indent=2)
    return {"exported": "openapi.json", "paths": len(schema["paths"])}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)