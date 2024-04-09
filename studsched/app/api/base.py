"""Endpoints for getting version information."""

from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from datetime import datetime

from ..db.queries import queries
from ..db.session import SessionLocal
from ..version import __version__
from ..schemas.base import (
    VersionResponse,
    SubjectResponse,
    SubjectStatus,
    Task,
    TaskType,
    Requirement,
    RequirementCreate,
    RequirementType,
    ThresholdType,
)

base_router = APIRouter()


@base_router.get("/version", response_model=VersionResponse)
async def version() -> Any:
    """Provide version information about the web service.

    \f
    Returns:
        VersionResponse: A json response containing the version number.
    """
    return VersionResponse(version=__version__)


@base_router.get("/subjects", response_model=list[SubjectResponse])
async def subjects() -> Any:
    tasks = [
        Task(
            max_points=10,
            deadline=datetime(2002, 1, 27, 1),
            task_type=TaskType.LAB,
        )
    ]
    requirements = [
        Requirement(
            id=0,
            task_type=TaskType.LAB,
            requirement_type=RequirementType.TOTAL,
            threshold=5,
            threshold_type=ThresholdType.POINTS,
        )
    ]
    subjects = [
        SubjectResponse(
            id="1",
            name="ZPRP",
            status=SubjectStatus.PASSED,
            tasks=tasks,
            requirements=requirements,
        )
    ]
    return subjects


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@base_router.post("/subjects/{subject_id}/requirements")
async def add_requirements(
    requirements: list[RequirementCreate],
    subject_id: int,
    db: Session = Depends(get_db),
):
    """Adds new requirement for a given subject"""

    return [
        queries.add_requirement(db, requirement)
        for requirement in requirements
    ]
