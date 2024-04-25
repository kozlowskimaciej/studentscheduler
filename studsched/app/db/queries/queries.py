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


def get_subjects(db: Session, user_id: int) -> list[models.Subject]:
    user = db.get_one(models.User, user_id)
    return [
        models.Subject(
            **linked_course.model_dump(),
            name=linked_course.course.name,
            status=models.SubjectStatus.IN_PROGRESS,
            requirements=linked_course.requirements
        )
        for linked_course in user.linked_courses
    ]


def add_user_info(db: Session, user_info: models.UserInfo):
    """Adds information about students and his/her courses"""

    db.add(user_info.user)

    for course in user_info.courses:
        db_course = models.Course(**course.model_dump())
        db.add(db_course)
        linked_course = models.LinkedCourse(
            user=user_info.user,
            course=db_course,
        )
        db.add(linked_course)

    db.commit()
    db.refresh(user_info.user)
