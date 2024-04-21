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


def get_subjects(db: Session) -> list[models.Subject]:
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


def add_user_info(db: Session, user_info: models.UserInfo):
    """Adds information about students and his/her courses"""

    user = models.User(**user_info.user.model_dump())
    db.add(user)

    for course in user_info.courses:
        db.add(models.Course(**course.model_dump()))
        linked_course = models.LinkedCourse()
        db.add(linked_course)
    db.commit()
