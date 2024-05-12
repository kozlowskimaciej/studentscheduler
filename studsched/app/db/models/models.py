"""Sqlmodel models"""
from datetime import datetime
from typing import Optional
from enum import IntEnum, auto

from sqlmodel import Field, SQLModel, Relationship


class TaskType(IntEnum):
    LAB = auto()
    EXAM = auto()
    COLL = auto()


class RequirementType(IntEnum):
    TOTAL = auto()
    SEPARATELY = auto()


class ThresholdType(IntEnum):
    PERCENT = auto()
    POINTS = auto()


class SubjectStatus(IntEnum):
    """Status of subject completion"""

    PASSED = auto()
    FAILED = auto()
    IN_PROGRESS = auto()


class VersionResponse(SQLModel):
    """Response for version endpoint."""

    version: str


class LinkedCourse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    requirements: list["Requirement"] = Relationship(back_populates="course")
    tasks: list["Task"] = Relationship(back_populates="course")


class RequirementBase(SQLModel):
    task_type: TaskType
    requirement_type: RequirementType
    threshold: int
    threshold_type: ThresholdType


class Requirement(RequirementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linked_course_id: int = Field(foreign_key="linkedcourse.id")

    course: LinkedCourse = Relationship(back_populates="requirements")


class RequirementCreate(RequirementBase):
    """Model for creating new requirement"""


class TaskBase(SQLModel):
    task_type: TaskType
    max_points: int
    points: int
    deadline: datetime


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linked_course_id: int = Field(foreign_key="linkedcourse.id")

    course: LinkedCourse = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Model for creating new tasks"""


class Subject(SQLModel):
    id: int
    name: str
    status: SubjectStatus
    requirements: list[Requirement]
    tasks: list[Task]
