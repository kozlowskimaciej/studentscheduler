"""Define response model for the endpoint version."""

from pydantic import BaseModel, Field  # type: ignore
from datetime import datetime
from enum import IntEnum, auto


class VersionResponse(BaseModel):
    """Response for version endpoint."""

    version: str = Field(..., example="1.0.0")


class TaskType(IntEnum):
    LAB = auto()
    EXAM = auto()
    KOL = auto()


class Task(BaseModel):
    """Single task that is needed to complete a subject"""

    max_points: int
    result: int
    deadline: datetime
    task_type: TaskType
    ended: bool
    description: str


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
