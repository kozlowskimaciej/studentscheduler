from sqlmodel import Session, select

from ...db.models import models


def add_requirement(
    db: Session, requirement: models.RequirementCreate, subject_id: int
) -> models.Requirement:
    db_requirement = models.Requirement(
        **requirement.model_dump(), linked_course_id=subject_id
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement


def update_requirement(
    db: Session, updated_requirement: models.RequirementPublic
):
    db_requirement = db.get(models.Requirement, updated_requirement.id)
    db_requirement.sqlmodel_update(updated_requirement.model_dump())
    db.add(db_requirement)
    db.commit()


def get_subjects(db: Session):
    statement = select(models.LinkedCourse)
    linked_courses = db.exec(statement).all()
    return [
        models.Subject(
            **linked_course.model_dump(),
            name="Subject",
            status=models.SubjectStatus.IN_PROGRESS,
            requirements=linked_course.requirements
        )
        for linked_course in linked_courses
    ]
