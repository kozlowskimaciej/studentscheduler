"""Endpoints for getting subjects information."""

from typing import Any
from sqlmodel import Session
from fastapi import APIRouter, Depends

from .base import get_db
from ..db.queries import queries
from ..db.models.models import (
    RequirementCreate,
    Course,
)

courses_router = APIRouter(prefix='/courses', tags=['courses'])


@courses_router.get("/", response_model=list[Course])
async def courses(db: Session = Depends(get_db)) -> Any:
    return queries.get_courses(db)


@courses_router.post("/{linked_course_id}/requirements")
async def add_requirements(
        requirements: list[RequirementCreate],
        linked_course_id: int,
        db: Session = Depends(get_db),
):
    """Adds new requirement for a given subject"""
    return [
        queries.add_requirement(db, requirement, linked_course_id)
        for requirement in requirements
    ]
