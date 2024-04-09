"""Sqlalchemy models"""

from sqlalchemy import Column, Integer, Enum

from ...schemas.base import TaskType, RequirementType, ThresholdType
from ..base import Base


class Requirement(Base):
    id = Column(Integer, primary_key=True)

    task_type = Column(Enum(TaskType))
    requirement_type = Column(Enum(RequirementType))
    threshold = Column(Integer)
    threshold_type = Column(Enum(ThresholdType))
