"""Endpoints for getting version information."""

from typing import Any
from sqlmodel import Session
from fastapi import APIRouter

from ..db.session import engine
from ..version import __version__
from ..db.models.models import (
    VersionResponse,
)

base_router = APIRouter(tags=['base'])


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
