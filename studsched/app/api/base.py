"""Endpoints for getting version information."""

from typing import Any
from fastapi import APIRouter
from ..schemas.base import (
    VersionResponse,
    SubjectListResponse,
    SubjectResponse,
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


@base_router.get("/subjects", response_model=SubjectListResponse)
async def henlo() -> Any:
    subjects = []
    subjects.append(SubjectResponse(id="1", name="ZPRP"))
    return SubjectListResponse(subjects=subjects)
