"""FastAPI application entry point.

Run locally with::

    cd backend
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .models import HealthResponse
from .routers import agents, providers, workloads

app = FastAPI(
    title="AI Workstation API",
    version=__version__,
    description="REST API serving the AI Workstation web home.",
)

# Allow the Vite dev server (and any locally hosted shell) to call us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


app.include_router(agents.router, prefix="/api")
app.include_router(providers.router, prefix="/api")
app.include_router(workloads.router, prefix="/api")
