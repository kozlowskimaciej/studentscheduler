"""Endpoints for getting version information."""

from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from ..db.queries import queries
from ..db.session import SessionLocal
from ..version import __version__
from ..schemas.base import VersionResponse, Subject, RequirementCreate

base_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
