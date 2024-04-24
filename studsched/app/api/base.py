"""Endpoints for getting version information."""

from typing import Any
from sqlmodel import Session
from fastapi import APIRouter, Depends

from ..db.queries import queries
from ..db.session import engine
from ..version import __version__
from ..db.models.models import (
    RequirementUpdate,
    VersionResponse,
    Subject,
)

base_router = APIRouter()


def get_db():
    with Session(engine) as session:
        yield session


@base_router.get("/version", response_model=VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return VersionResponse(version=__version__)


@base_router.get("/subjects", response_model=list[Subject])
async def subjects(db: Session = Depends(get_db)) -> Any:
    return queries.get_subjects(db)


@base_router.put("/subjects/{subject_id}/requirements")
async def replace_requirements(
    subject_id: int,
    requirements: list[RequirementUpdate],
    db: Session = Depends(get_db),
):
    queries.replace_requirements(db, subject_id, requirements)
