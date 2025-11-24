# app/routers/tasks.py
"""
CRUD endpoints for Task.

We expose:
- GET /tasks          -> list all tasks
- GET /tasks/{id}     -> get a single task
- POST /tasks         -> create a task
- PUT /tasks/{id}     -> update a task
- DELETE /tasks/{id}  -> delete a task
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.task_models import Task as TaskModel
from ..schemas.task_schemas import Task, TaskCreate, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=List[Task])
def list_tasks(
    completed: bool | None = Query(
        default=None,
        description="Optional filter by completion status.",
    ),
    db: Session = Depends(get_db),
) -> List[Task]:
    """
    Return all tasks, optionally filtered by completion status.
    """
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter(TaskModel.completed == completed)
    tasks = query.all()
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    """
    Return a single task by its ID.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    """
    Create a new task.
    """
    task = TaskModel(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    """
    Update an existing task (partial update).
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete an existing task.
    """
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()
