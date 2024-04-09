"""Endpoints for getting version information."""

from typing import Any
from fastapi import APIRouter
from ..schemas.base import (
    VersionResponse,
    SubjectResponse,
    SubjectStatus,
    Task,
    TaskType,
    Requirement,
    RequirementType,
    ThresholdType,
)
from ..version import __version__
from datetime import datetime

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


@base_router.post("/subjects/{subject_id}/requirements")
async def add_requirements(
    requirements: list[Requirement],
    subject_id: int,
) -> list[Requirement]:
    """Adds new requirement for a given subject"""

    # Do some db staff
    return requirements  # Return newly created requirement
