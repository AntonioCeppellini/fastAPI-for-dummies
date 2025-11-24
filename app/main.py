# app/main.py
"""
FastAPI application entrypoint.

Here we:
- Create the FastAPI app instance
- Configure CORS for the frontend SPA
- Create database tables at startup
- Include the tasks router
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .models import task_models as task_model  # noqa: F401 (import needed for table creation)
from .routers import task_views as tasks_router


# Create all tables.
# For a real project, you would use Alembic migrations instead of create_all().
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Tasks API",
    description="Simple CRUD API for tasks, used as a coding test example.",
    version="0.1.0",
)


# CORS configuration:
# This allows a frontend (e.g. React, Vue, Angular) running on a different
# origin (port/host) to call our API via browser.
origins = [
    "http://localhost:5173",  # Example for Vite-based frontend
    "http://localhost:3000",  # Example for classic React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # In production, restrict this properly
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods: GET, POST, etc.
    allow_headers=["*"],          # Allow all headers
)


# Include routers
app.include_router(tasks_router.router)


@app.get("/health")
def health_check():
    """
    Simple health-check endpoint.

    Useful for quick check that the app is running.
    """
    return {"status": "ok"}
