from fastapi import FastAPI, HTTPException, status, Query, Path
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

app = FastAPI(title="Models & Validation", description="Pydantic models, request bodies, and validation")


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Tag(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    color: str = Field(default="blue")


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, examples=["Buy groceries"])
    description: Optional[str] = Field(None, max_length=500)
    priority: Priority = Priority.medium
    tags: List[Tag] = []
    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_must_be_meaningful(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError("Title cannot be blank")
        return v.strip()


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: Priority
    tags: List[Tag]
    done: bool
    due_date: Optional[datetime]
    created_at: datetime


tasks_db: dict[int, dict] = {}
task_id_counter: int = 0


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global task_id_counter
    task_id_counter += 1
    now = datetime.now()
    record = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "tags": [t.model_dump() for t in task.tags],
        "done": False,
        "due_date": task.due_date,
        "created_at": now,
    }
    tasks_db[task_id_counter] = record
    return record


@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(priority: Optional[Priority] = None, done: Optional[bool] = None):
    results = list(tasks_db.values())
    if priority:
        results = [t for t in results if t["priority"] == priority]
    if done is not None:
        results = [t for t in results if t["done"] == done]
    return results


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int = Path(..., ge=1)):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/search")
def search_tasks(q: str = Query(..., min_length=2, description="Search query")):
    results = [
        t for t in tasks_db.values()
        if q.lower() in t["title"].lower() or (t["description"] and q.lower() in t["description"].lower())
    ]
    return {"query": q, "count": len(results), "results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
