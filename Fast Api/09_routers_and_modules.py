"""
===============================================================================
Lesson 09: Routers & Modular Application Structure (`APIRouter`)
===============================================================================
80/20 Principle Focus:
- Structuring scalable FastAPI applications using `APIRouter`
- Splitting code into domain modules (e.g., users, items, auth)
- Mounting routers using `app.include_router()`
- Configuring URL prefixes (`prefix="/api/v1/users"`) and OpenAPI tags
- Global and Router-level dependencies

How to Run:
   python 09_routers_and_modules.py
Interactive Docs Test:
- Open http://127.0.0.1:8000/docs
- Notice how the endpoints are neatly grouped under 'Users' and 'Products' tags!
===============================================================================
"""

from fastapi import FastAPI, APIRouter, Depends, Header, HTTPException, status
import uvicorn

# Main FastAPI App Instance
app = FastAPI(
    title="FastAPI 80/20 - Lesson 09: APIRouter & Modular Code",
    description="Learn how to split large FastAPI apps into clean, modular APIRouter modules.",
    version="1.0.0",
)


# =============================================================================
# MODULE 1: Users Router (`/api/v1/users`)
# =============================================================================
users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users Module"],  # Groups these routes together in /docs!
    responses={404: {"description": "User resource not found"}},
)


@users_router.get("/")
def list_users():
    """GET /api/v1/users/"""
    return [
        {"id": 1, "username": "alice", "role": "admin"},
        {"id": 2, "username": "bob", "role": "developer"},
    ]


@users_router.get("/{user_id}")
def get_user_profile(user_id: int):
    """GET /api/v1/users/{user_id}"""
    return {"id": user_id, "username": f"user_{user_id}", "status": "active"}


# =============================================================================
# MODULE 2: Products Router (`/api/v1/products`)
# =============================================================================
products_router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products Module"],
)


@products_router.get("/")
def list_products():
    """GET /api/v1/products/"""
    return [
        {"id": 101, "name": "Laptop", "price": 1200.0},
        {"id": 102, "name": "Monitor", "price": 300.0},
    ]


@products_router.get("/{product_id}")
def get_product(product_id: int):
    """GET /api/v1/products/{product_id}"""
    return {"id": product_id, "name": f"Product #{product_id}", "in_stock": True}


# =============================================================================
# MODULE 3: Admin Router with Router-Level Dependencies (`/api/v1/admin`)
# =============================================================================
def verify_admin_role(x_admin_token: str = Header(...)):
    if x_admin_token != "super-admin-secret":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin token invalid or unauthorized.",
        )


admin_router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin Management"],
    dependencies=[Depends(verify_admin_role)],  # Applied to ALL routes in this router!
)


@admin_router.get("/metrics")
def get_system_metrics():
    """GET /api/v1/admin/metrics (Requires X-Admin-Token header)"""
    return {"cpu_usage": "15%", "memory_usage": "42%", "active_sessions": 128}


# =============================================================================
# MOUNT ROUTERS INTO MAIN APP
# =============================================================================
app.include_router(users_router)
app.include_router(products_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Modular FastAPI!",
        "available_modules": [
            "/api/v1/users",
            "/api/v1/products",
            "/api/v1/admin",
        ],
        "docs": "http://127.0.0.1:8000/docs",
    }


if __name__ == "__main__":
    uvicorn.run("09_routers_and_modules:app", host="127.0.0.1", port=8000, reload=True)
