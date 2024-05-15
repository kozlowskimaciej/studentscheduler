"""Endpoints for getting version information."""

from typing import Any, Annotated
from sqlmodel import Session
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm.exc import NoResultFound

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
    user_id = request.session.get("user_id")
    return db.get(models.User, user_id)


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]


@base_router.get("/subjects", response_model=list[models.Subject])
async def subjects(user: CurrentUserDep):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No current user"
        )
    return queries.get_subjects(user)


@base_router.put("/subjects/{subject_id}/requirements")
async def replace_requirements(
    requirements: list[models.RequirementCreate],
    subject_id: int,
    db: DatabaseDep,
):
    try:
        queries.replace_requirements(db, subject_id, requirements)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found",
        )


@base_router.put("/subjects/{subject_id}/tasks")
async def replace_tasks(
    subject_id: int,
    tasks: list[models.TaskCreate],
    db: Session = Depends(get_db),
):
    try:
        queries.replace_tasks(db, subject_id, tasks)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found",
        )
