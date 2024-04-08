"""Endpoints for getting version information."""

from typing import Any
from fastapi import APIRouter
from ..schemas.base import (
    VersionResponse,
    SubjectResponse,
    SubjectStatus,
)
from ..version import __version__

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
async def henlo() -> Any:
    subjects = []
    subjects.append(
        SubjectResponse(
            id="1", name="ZPRP", status=SubjectStatus.PASSED, tasks=[]
        )
    )
    return subjects
