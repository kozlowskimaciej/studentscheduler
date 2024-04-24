from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, replace_requirements
from studsched.app.db.models import models
import pytest
from sqlalchemy.orm.exc import NoResultFound


def test_get_subjects_empty(db_session: Session):
    res = get_subjects(db_session)
    assert res == []


def test_get_subjects(filled_db: Session):
    res = get_subjects(filled_db)
    assert len(res) == 1


def test_replace_requirements(
    filled_db: Session,
    linked_course: models.LinkedCourse,
    requirement: models.Requirement,
):
    subjects = get_subjects(filled_db)
    requirements = subjects[0].requirements
    assert len(requirements) == 1

    requirement_update = models.RequirementCreate(**requirement.model_dump())
    replace_requirements(filled_db, linked_course.id, [requirement_update] * 2)

    subjects = get_subjects(filled_db)
    requirements = subjects[0].requirements
    assert len(requirements) == 2


def test_delete_requirements(
    filled_db: Session,
    linked_course: models.LinkedCourse,
):
    subjects = get_subjects(filled_db)
    requirements = subjects[0].requirements
    assert len(requirements) == 1

    replace_requirements(filled_db, linked_course.id, [])

    subjects = get_subjects(filled_db)
    requirements = subjects[0].requirements
    assert len(requirements) == 0


def test_replace_requirements_invalid_linked_course(
    db_session: Session,
):
    invalid_linked_course_id = 234

    with pytest.raises(NoResultFound):
        replace_requirements(db_session, invalid_linked_course_id, [])
