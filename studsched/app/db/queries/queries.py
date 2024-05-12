from sqlmodel import Session, select, delete

from ...db.models import models


def replace_requirements(
    db: Session,
    linked_course_id: int,
    new_requirements: list[models.RequirementCreate],
):
    """Replace all subject's requirements with new ones"""

    linked_course = db.get_one(models.LinkedCourse, linked_course_id)
    for requirement in linked_course.requirements:
        db.delete(requirement)

    db.add_all(
        models.Requirement(
            **requirement.model_dump(),
            linked_course_id=linked_course_id,
        )
        for requirement in new_requirements
    )

    db.commit()


def replace_tasks(
    db: Session,
    linked_course_id: int,
    new_tasks: list[models.TaskCreate],
):
    """Replace all subject's requirements with new ones"""

    linked_course = db.get_one(models.LinkedCourse, linked_course_id)
    for task in linked_course.tasks:
        db.delete(task)

    db.add_all(
        models.Task(
            **task.model_dump(),
            linked_course_id=linked_course_id,
        )
        for task in new_tasks
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
            tasks=linked_course.tasks,
        )
        for linked_course in linked_courses
    ]
