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


def get_subjects(user: models.User) -> list[models.Subject]:
    return [
        models.Subject(
            **linked_course.model_dump(),
            name=linked_course.course.name,
            status=models.SubjectStatus.IN_PROGRESS,
            requirements=linked_course.requirements
        )
        for linked_course in user.linked_courses
    ]


def try_add_user(db: Session, user: models.UserCreate) -> models.User:
    user_select = select(models.User).where(models.User.index == user.index)
    db_user = db.exec(user_select).first()

    if db_user is None:
        db_user = models.User(**user.model_dump())
        db.add(db_user)

    return db_user


def try_add_course(db: Session, course: models.CourseCreate) -> models.Course:
    course_select = select(models.Course).where(
        models.Course.code == course.code
    )
    db_course = db.exec(course_select).first()

    if db_course is None:
        db_course = models.Course(**course.model_dump())
        db.add(db_course)

    return db_course


def try_add_linked_course(
    db: Session, user: models.User, course: models.Course
) -> None:
    select_linked_course = (
        select(models.LinkedCourse)
        .where(models.LinkedCourse.user_id == user.id)
        .where(models.LinkedCourse.course_id == course.id)
    )
    db_linked_course = db.exec(select_linked_course).first()

    if db_linked_course is None:
        linked_course = models.LinkedCourse(
            user=user,
            course=course,
        )
        db.add(linked_course)


def add_user_info(db: Session, user_info: models.UserInfo):
    """Adds information about users and their courses if it's missing"""

    db_user = try_add_user(db, user_info.user)

    for course in user_info.courses:
        db_course = try_add_course(db, course)
        try_add_linked_course(db, user=db_user, course=db_course)

    db.commit()
    return db_user
