from sqlmodel import Session, select, delete

from ...db.models import models


def replace_requirements(
    db: Session,
    linked_course_id: int,
    new_requirements: list[models.RequirementCreate],
):
    """Replace all subject's requirements with new ones"""

    delete_statement = delete(models.Requirement).where(
        models.Requirement.linked_course_id == linked_course_id
    )
    db.exec(delete_statement)

    db.add_all(
        models.Requirement(
            **requirement.model_dump(),
            linked_course_id=linked_course_id,
        )
        for requirement in new_requirements
    )

    db.commit()


def get_subjects(db: Session):
    statement = select(models.LinkedCourse)
    linked_courses = db.exec(statement).all()
    return [
        models.Subject(
            **linked_course.model_dump(),
            name="Subject",
            status=models.SubjectStatus.IN_PROGRESS,
            requirements=linked_course.requirements,
        )
        for linked_course in linked_courses
    ]
