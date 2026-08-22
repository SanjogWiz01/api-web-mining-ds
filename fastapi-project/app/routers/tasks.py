"""
Tasks router — full CRUD endpoints for task management.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task as task_service
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="List all tasks",
)
def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max tasks to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve all tasks belonging to the authenticated user.
    Supports pagination via `skip` and `limit` query parameters.
    """
    return task_service.get_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201,
    summary="Create a new task",
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new task for the authenticated user.

    - **title**: Task title (required)
    - **description**: Optional detailed description
    - **priority**: low, medium, high, or critical (default: medium)
    - **due_date**: Optional deadline
    """
    return task_service.create_task(db, task_data, owner_id=current_user.id)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retrieve a specific task by its ID. Only the task owner can access it."""
    return task_service.get_task_by_id(db, task_id, owner_id=current_user.id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update an existing task. Only provided fields will be changed.
    Marking `is_completed=true` automatically sets status to `done`.
    """
    return task_service.update_task(db, task_id, task_data, owner_id=current_user.id)


@router.delete(
    "/{task_id}",
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a task by its ID. Only the task owner can delete it."""
    return task_service.delete_task(db, task_id, owner_id=current_user.id)
