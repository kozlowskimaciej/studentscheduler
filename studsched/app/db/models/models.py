"""Sqlalchemy models"""

from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from ...schemas.base import TaskType, RequirementType, ThresholdType
from ..base import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True)
    task_type = Column(Enum(TaskType))
    requirement_type = Column(Enum(RequirementType))
    threshold = Column(Integer)
    threshold_type = Column(Enum(ThresholdType))
    linked_course_id = Column(Integer, ForeignKey("linked_course.id"))

    course = relationship("LinkedCourse", back_populates="requirements")


class LinkedCourse(Base):
    __tablename__ = "linked_course"

    id = Column(Integer, primary_key=True)

    requirements = relationship("Requirement", back_populates="course")
