"""Define response model for the endpoint version."""

from pydantic import BaseModel, Field  # type: ignore
from datetime import datetime
from enum import StrEnum, auto
from typing import Optional


class VersionResponse(BaseModel):
    """Response for version endpoint."""

    version: str = Field(..., example="1.0.0")


class TaskType(StrEnum):
    LAB = auto()
    EXAM = auto()
    COLL = auto()


class Task(BaseModel):
    """Subject task that helps to complete a subject"""

    max_points: int
    result: Optional[int]
    deadline: datetime
    task_type: TaskType
    ended: bool = False
    description: str = ""


class RequirementType(StrEnum):
    TOTAL = auto()
    SEPARATELY = auto()


class ThresholdType(StrEnum):
    PERCENT = auto()
    POINTS = auto()


class RequirementBase(BaseModel):
    task_type: TaskType
    requirement_type: RequirementType
    threshold: int
    threshold_type: ThresholdType


class RequirementCreate(RequirementBase):
    """Model for creating subject requirement"""


class Requirement(RequirementBase):
    """Requirement that is needed to pass a subject"""

    id: int

    class Config:
        orm_mode = True


class SubjectStatus(StrEnum):
    """Status of subject completion"""

    PASSED = auto()
    FAILED = auto()
    IN_PROGRESS = auto()


class Subject(BaseModel):
    """Subject with its requirements"""

    id: str
    name: str
    status: SubjectStatus
    # tasks: list[Task]
    requirements: list[Requirement]

    class Config:
        orm_mode = True
