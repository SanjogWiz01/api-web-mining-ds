"""
Task service — business logic for CRUD operations on tasks.
"""

from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
    """Retrieve all tasks belonging to a specific user."""
    return (
        db.query(Task)
        .filter(Task.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Task:
    """
    Retrieve a single task by its ID, ensuring it belongs to the requesting user.
    Raises 404 if not found or not owned.
    """
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    """Create a new task for the given user."""
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        owner_id=owner_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_data: TaskUpdate, owner_id: int) -> Task:
    """
    Update an existing task. Only provided (non-None) fields are updated.
    """
    task = get_task_by_id(db, task_id, owner_id)

    update_fields = task_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(task, field, value)

    # Auto-set status to DONE when marked complete
    if task_data.is_completed is True:
        task.status = "done"

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, owner_id: int) -> dict:
    """Delete a task by its ID. Returns a confirmation message."""
    task = get_task_by_id(db, task_id, owner_id)
    db.delete(task)
    db.commit()
    return {"detail": f"Task '{task.title}' deleted successfully"}
