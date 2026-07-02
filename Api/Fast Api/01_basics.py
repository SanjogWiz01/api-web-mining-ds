from fastapi import FastAPI, HTTPException, status
from typing import Optional

app = FastAPI(title="FastAPI Basics", description="Intro to path params, query params, and CRUD")

fake_db = {
    1: {"id": 1, "title": "Learn Python", "done": False},
    2: {"id": 2, "title": "Build an API", "done": False},
    3: {"id": 3, "title": "Deploy to production", "done": True},
}


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!", "docs": "/docs"}


@app.get("/tasks")
def list_tasks(done: Optional[bool] = None):
    if done is None:
        return list(fake_db.values())
    return [t for t in fake_db.values() if t["done"] == done]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = fake_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(title: str):
    new_id = max(fake_db.keys()) + 1 if fake_db else 1
    task = {"id": new_id, "title": title, "done": False}
    fake_db[new_id] = task
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: Optional[str] = None, done: Optional[bool] = None):
    task = fake_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if title is not None:
        task["title"] = title
    if done is not None:
        task["done"] = done
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = fake_db.pop(task_id, None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted", "task": task}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
