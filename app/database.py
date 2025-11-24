# app/database.py
"""
Database configuration module.

Here we:
- Configure the SQLite database URL
- Create the SQLAlchemy engine
- Create a SessionLocal class to get DB sessions
- Define a Base class for our models
- Provide a get_db() dependency for FastAPI endpoints
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# SQLite database URL.
# "sqlite:///./app.db" means: create/use app.db in the current directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"


# For SQLite, we need this connect_args check_same_thread=False
# because the default SQLite driver is not fully thread-safe.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# SessionLocal is a factory that will create new Session objects.
# We use autocommit=False and autoflush=False for explicit control.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Every ORM model will inherit from this.
    """
    pass


def get_db() -> Generator:
    """
    Dependency used in FastAPI endpoints to get a database session.

    Usage in endpoints:
        db: Session = Depends(get_db)

    It yields a session and makes sure to close it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

