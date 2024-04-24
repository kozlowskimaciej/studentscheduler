"""Endpoints for getting version information."""

from typing import Any
from sqlmodel import Session
from fastapi import APIRouter, Depends, status

from ..db.queries import queries
from ..db.session import engine
from ..version import __version__
from ..db.models.models import (
    RequirementCreate,
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


@base_router.post("/subjects/{subject_id}/requirements")
async def add_requirements(
    requirements: list[RequirementCreate],
    subject_id: int,
    db: Session = Depends(get_db),
):
    """Adds new requirement for a given subject"""
    return [
        queries.add_requirement(db, requirement, subject_id)
        for requirement in requirements
    ]


@base_router.put(
    "/subjects/{subject_id}/requirements/{requirement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_requirement(
    subject_id: int,
    requirement_id: int,
    requirement: RequirementUpdate,
    db: Session = Depends(get_db),
):
    queries.update_requirement(db, requirement_id, requirement)
