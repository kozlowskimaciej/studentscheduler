"""Define response model for the endpoint version."""

from pydantic import BaseModel, Field  # type: ignore
from datetime import datetime
from enum import IntEnum, auto
from typing import Optional


class VersionResponse(BaseModel):
    """Response for version endpoint."""

    version: str = Field(..., example="1.0.0")


class TaskType(IntEnum):
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


class RequirementType(IntEnum):
    TOTAL = auto()
    SEPARATELY = auto()


class ThresholdType(IntEnum):
    PERCENT = auto()
    POINTS = auto()


class Requirement(BaseModel):
    """Subject requirement that is needed to pass"""

    task_type: TaskType
    requirement_type: RequirementType
    threshold: int
    threshold_type: ThresholdType


class SubjectStatus(IntEnum):
    """Status of subject completion"""

    PASSED = auto()
    FAILED = auto()
    IN_PROGRESS = auto()


class SubjectResponse(BaseModel):
    """Subject with its requirements"""

    id: str
    name: str
    status: SubjectStatus
    tasks: list[Task]
    requirements: list[Requirement]
