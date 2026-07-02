from fastapi import FastAPI, HTTPException, Depends, Header, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio
import random

app = FastAPI(title="Async & Dependencies", description="Async handlers, dependency injection, background tasks")


fake_users = {
    "alice": {"role": "admin", "email": "alice@example.com"},
    "bob": {"role": "user", "email": "bob@example.com"},
}


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime


posts_db: dict[int, Post] = {}
post_id_counter = 0


async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    user = fake_users.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": token, **user}


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@app.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.get("/admin")
async def admin_panel(current_user: dict = Depends(require_admin)):
    return {"message": f"Welcome admin {current_user['username']}", "secret": "top-secret-data"}


async def slow_operation(delay: float = 1.0):
    await asyncio.sleep(delay)
    return {"result": random.randint(1, 100), "delay": delay}


@app.get("/async")
async def async_endpoint():
    results = await asyncio.gather(
        slow_operation(0.5),
        slow_operation(1.0),
        slow_operation(0.8),
    )
    return {"parallel_results": results}


def write_audit_log(post_id: int, action: str):
    with open("audit.log", "a") as f:
        f.write(f"[{datetime.now()}] {action}: post {post_id}\n")


@app.post("/posts", status_code=201)
async def create_post(
    title: str,
    content: str,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
):
    global post_id_counter
    post_id_counter += 1
    post = Post(
        id=post_id_counter,
        title=title,
        content=content,
        author=current_user["username"],
        created_at=datetime.now(),
    )
    posts_db[post_id_counter] = post

    background_tasks.add_task(write_audit_log, post_id_counter, "CREATE")

    return post


@app.get("/posts", response_model=List[Post])
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
):
    all_posts = list(posts_db.values())
    return all_posts[skip : skip + limit]


@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int, current_user: dict = Depends(get_current_user)):
    post = posts_db.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
