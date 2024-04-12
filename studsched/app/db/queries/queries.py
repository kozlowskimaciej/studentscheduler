from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

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


def get_subjects(db: Session):
    linked_courses = db.scalars(
        select(models.LinkedCourse).options(
            joinedload(models.LinkedCourse.requirements)
        )
    )
    return [
        schemas.Subject(
            **linked_course._asdict(),
            name="Subject",
            status=schemas.SubjectStatus.IN_PROGRESS,
            requirements=linked_course.requirements
        )
        for linked_course in linked_courses.unique().all()
    ]
