"""Sqlmodel models"""

from sqlmodel import SQLModel, Field, Relationship
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

    index: str = Field(sa_column_kwargs={"unique": True})
    first_name: str
    middle_names: Optional[str] = None
    last_name: str
    email: str
    last_login: datetime


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    linked_courses: list["LinkedCourse"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    "Model for creating new user"


class UserPublic(UserBase):
    id: int


class CourseBase(SQLModel):
    """A course that students can take"""

    name: str
    code: str = Field(sa_column_kwargs={"unique": True})


class CourseCreate(CourseBase):
    """Model for creating new course"""


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    linked_courses: list["LinkedCourse"] = Relationship(
        back_populates="course"
    )


class LinkedCourse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    course_id: int = Field(foreign_key="course.id")

    user: User = Relationship(back_populates="linked_courses")
    course: Course = Relationship(back_populates="linked_courses")
    requirements: list["Requirement"] = Relationship(
        back_populates="linked_course"
    )


class RequirementBase(SQLModel):
    task_type: TaskType
    requirement_type: RequirementType
    threshold: int
    threshold_type: ThresholdType


class Requirement(RequirementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    linked_course_id: int = Field(foreign_key="linkedcourse.id")

    linked_course: LinkedCourse = Relationship(back_populates="requirements")


class RequirementCreate(RequirementBase):
    """Model for creating new requirement"""


class Subject(SQLModel):
    """
    Model for retrieving data about a subject.
    It is not even reflected in any database table.
    """

    id: int
    name: str
    status: SubjectStatus
    requirements: list[Requirement]


class UserInfo(SQLModel):
    """
    User with his/her courses.
    Used to add all necessary data after the user logs in.
    """

    user: UserCreate
    courses: list[CourseCreate]
