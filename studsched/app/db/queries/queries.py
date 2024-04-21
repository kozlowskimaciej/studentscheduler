from sqlmodel import Session, select

from ...db.models import models


def add_requirement(
    db: Session, requirement: models.RequirementCreate, linked_course_id: int
) -> models.Requirement:
    db_requirement = models.Requirement(
        **requirement.model_dump(), linked_course_id=linked_course_id
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement


def delete_requirement(
        db: Session, requirement_id: int
) -> None:
    statement = select(models.Requirement) \
                .where(models.Requirement == requirement_id)
    req = db.exec(statement).all()
    assert len(req) == 1, f'Requirement id {requirement_id} not found'
    db.delete(req[0])
    db.commit()


def get_courses(db: Session):
    statement = select(models.LinkedCourse)
    linked_courses = db.exec(statement).all()
    return [
        models.Course(
            **linked_course.model_dump(),
            name="Course",
            status=models.CourseStatus.IN_PROGRESS,
            requirements=linked_course.requirements
        )
        for linked_course in linked_courses
    ]
