"""Sqlmodel models"""

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime

from enum import IntEnum, auto


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


class UserBase(SQLModel):
    """A student"""

    first_name: str
    middle_names: Optional[str]
    last_name: str
    email: str
    last_login: datetime


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    "Model for creating new user"


class UserPublic(UserBase):
    id: int


class CourseBase(SQLModel):
    """A course that students can take"""

    name: str
    code: str


class CourseCreate(CourseBase):
    """Model for creating new course"""


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class LinkedCourse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    requirements: list["Requirement"] = Relationship(back_populates="course")


class RequirementBase(SQLModel):
    task_type: TaskType
    requirement_type: RequirementType
    threshold: int
    threshold_type: ThresholdType


class Requirement(RequirementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linked_course_id: int = Field(default=None, foreign_key="linkedcourse.id")

    course: LinkedCourse = Relationship(back_populates="requirements")


class RequirementCreate(RequirementBase):
    """Model for creating new requirement"""


class Subject(SQLModel):
    id: int
    name: str
    status: SubjectStatus
    requirements: list[Requirement]


class UserInfo(SQLModel):
    """User with his/her courses"""

    user: User
    courses: list[CourseCreate]
