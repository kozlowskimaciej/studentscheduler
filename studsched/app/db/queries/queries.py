from sqlalchemy.orm import Session

from ...schemas import base as schemas
from ...db.models import models


def add_requirement(
    db: Session, requirement: schemas.RequirementCreate, subject_id: int
) -> models.Requirement:
    db_requirement = models.Requirement(
        **requirement.dict(), linked_course_id=subject_id
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement
