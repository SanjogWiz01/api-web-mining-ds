"""
Pydantic schemas for Task-related requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task import TaskPriority, TaskStatus


# ---------- Request Schemas ----------

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, examples=["Buy groceries"])
    description: Optional[str] = Field(None, max_length=1000, examples=["Milk, eggs, bread"])
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None


# ---------- Response Schemas ----------

class TaskResponse(BaseModel):
    """Schema for task data returned in API responses."""
    id: int
    title: str
    description: Optional[str] = None
    priority: TaskPriority
    status: TaskStatus
    is_completed: bool
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}
