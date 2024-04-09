from sqlalchemy.orm import Session

from ...schemas import base as schemas
from ...db.models import models


def add_requirement(
    db: Session, requirement: schemas.RequirementCreate
) -> models.Requirement:
    db_requirement = models.Requirement(**requirement.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement
