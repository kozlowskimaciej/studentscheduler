"""Endpoints for getting version information."""

from typing import Any
from sqlmodel import Session
from fastapi import APIRouter, Depends, Request

from ..db.queries import queries
from ..db.session import engine
from ..version import __version__
from ..db.models import models

base_router = APIRouter()


def get_db():
    with Session(engine) as session:
        yield session


@base_router.get("/version", response_model=models.VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return models.VersionResponse(version=__version__)


def get_current_user(request: Request):
    return request.session["user"]


@base_router.get("/subjects", response_model=list[models.Subject])
async def subjects(request: Request) -> Any:
    user = get_current_user(request)
    return queries.get_subjects(user)


@base_router.post("/subjects/{subject_id}/requirements")
async def add_requirements(
    requirements: list[models.RequirementCreate],
    subject_id: int,
    db: Session = Depends(get_db),
):
    """Adds new requirement for a given subject"""
    return [
        queries.add_requirement(db, requirement, subject_id)
        for requirement in requirements
    ]
