# app/models/task.py
"""
SQLAlchemy ORM model for the Task entity.

This defines the actual database table structure.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Task(Base):
    """
    Task model mapped to the "tasks" table.

    Fields:
    - id: primary key
    - title: short title
    - description: optional longer text
    - completed: boolean flag
    - priority: integer from 1 to 5 (we enforce the range at Pydantic level)
    - due_date: optional datetime deadline
    - owner_email: optional string email (validated at Pydantic level)
    - category: string category (validated at Pydantic level)
    - created_at / updated_at: timestamps
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    owner_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

