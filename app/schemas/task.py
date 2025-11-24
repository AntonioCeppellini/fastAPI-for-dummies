# app/schemas/task.py
"""
Pydantic schemas for Task.

Pydantic is used to:
- validate incoming data (request bodies)
- define the shape of outgoing data (responses)
- convert data to/from JSON
"""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class TaskBase(BaseModel):
    """
    Common fields for a Task.

    This class is not used directly in the API,
    but is inherited by other schemas to avoid duplication.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Short title of the task.",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional detailed description of the task.",
    )

    completed: bool = Field(
        default=False,
        description="Whether the task is completed or not.",
    )

    priority: int = Field(
        default=3,
        ge=1,
        le=5,
        description=(
            "Priority level from 1 (very low) to 5 (very high). "
            "Default is 3 (normal priority)."
        ),
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date for the task (deadline).",
    )

    owner_email: Optional[EmailStr] = Field(
        default=None,
        description="Optional email of the person responsible for this task.",
    )

    category: Optional[Literal["work", "personal", "study", "other"]] = Field(
        default="other",
        description="Category of the task.",
    )


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.

    We reuse TaskBase fields.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields are optional because we support partial updates.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Short title of the task.",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional detailed description of the task.",
    )

    completed: Optional[bool] = Field(
        default=None,
        description="Whether the task is completed or not.",
    )

    priority: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
        description="Priority level from 1 (very low) to 5 (very high).",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Optional due date for the task (deadline).",
    )

    owner_email: Optional[EmailStr] = Field(
        default=None,
        description="Optional email of the person responsible for this task.",
    )

    category: Optional[Literal["work", "personal", "study", "other"]] = Field(
        default=None,
        description="Category of the task.",
    )


class Task(TaskBase):
    """
    Schema used for reading tasks (API responses).

    It includes:
    - database ID
    - timestamps
    """

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # This tells Pydantic it can read data from ORM objects (SQLAlchemy models).
        from_attributes = True

