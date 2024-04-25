"""Endpoints for getting version information."""

from typing import Any
from sqlmodel import Session
from fastapi import APIRouter, Depends, Request

from ..db.queries import queries
from ..db.session import engine
from ..version import __version__
from ..db.models.models import (
    RequirementCreate,
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


def get_current_user_id(request: Request):
    return request.session["user_id"]


@base_router.get("/subjects", response_model=list[Subject])
async def subjects(request: Request, db: Session = Depends(get_db)) -> Any:
    user_id = get_current_user_id(request)
    return queries.get_subjects(db, user_id)


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
