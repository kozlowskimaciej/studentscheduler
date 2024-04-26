"""Endpoints for getting version information."""

from typing import Any, Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, Request

from ..db.session import engine
from ..version import __version__
from ..db.models import models
from ..db.queries import queries

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


DatabaseDep = Annotated[Session, Depends(get_db)]


def get_current_user(request: Request, db: DatabaseDep):
    user_id = request.session["user_id"]
    return db.get_one(models.User, user_id)


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]


@base_router.get("/subjects", response_model=list[models.Subject])
async def subjects(user: CurrentUserDep):
    return queries.get_subjects(user)


@base_router.post("/subjects/{subject_id}/requirements")
async def add_requirements(
    requirements: list[models.RequirementCreate],
    subject_id: int,
    db: DatabaseDep,
):
    """Adds new requirement for a given subject"""
    return [
        queries.add_requirement(db, requirement, subject_id)
        for requirement in requirements
    ]
