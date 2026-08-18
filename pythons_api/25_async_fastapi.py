"""Real implementation: async FastAPI with external HTTP calls.

FastAPI supports `async def` endpoints natively. Combine with httpx
AsyncClient to call other APIs without blocking the event loop.

Run:
    pip install fastapi "uvicorn[standard]" httpx
    python 25_async_fastapi.py
Then:  curl http://127.0.0.1:8000/posts/1
"""

import asyncio
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException

JSON_PLACEHOLDER = "https://jsonplaceholder.typicode.com"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=10.0, headers={"Accept": "application/json"})
    yield
    await app.state.http.aclose()


app = FastAPI(title="Async API", version="1.0.0", lifespan=lifespan)


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Calls JSONPlaceholder without blocking other requests."""
    client: httpx.AsyncClient = app.state.http
    try:
        r = await client.get(f"{JSON_PLACEHOLDER}/posts/{post_id}")
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="upstream error") from exc

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    r.raise_for_status()
    return r.json()


@app.get("/posts/{post_id}/comments")
async def get_post_with_comments(post_id: int):
    """Fetch post + comments concurrently using asyncio.gather."""
    client: httpx.AsyncClient = app.state.http

    async def fetch(path: str) -> httpx.Response:
        r = await client.get(f"{JSON_PLACEHOLDER}{path}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Post not found")
        r.raise_for_status()
        return r

    post_r, comments_r = await asyncio.gather(
        fetch(f"/posts/{post_id}"),
        fetch(f"/posts/{post_id}/comments"),
    )
    return {"post": post_r.json(), "comments": comments_r.json()}


@app.get("/many/{count}")
async def fetch_many(count: int):
    """Download `count` posts concurrently (bounded)."""
    count = max(1, min(count, 20))
    client: httpx.AsyncClient = app.state.http

    sem = asyncio.Semaphore(5)

    async def one(i: int) -> dict:
        async with sem:
            r = await client.get(f"{JSON_PLACEHOLDER}/posts/{i}")
            r.raise_for_status()
            return r.json()

    return await asyncio.gather(*(one(i) for i in range(1, count + 1)))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
