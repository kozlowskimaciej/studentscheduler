from sqlmodel import Session
from studsched.app.db.queries.queries import get_subjects, replace_requirements
from studsched.app.db.models import models


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

    requirement_update = models.RequirementUpdate(**requirement.model_dump())
    replace_requirements(filled_db, linked_course.id, [requirement_update] * 2)

    subjects = get_subjects(filled_db)
    requirements = subjects[0].requirements
    assert len(requirements) == 2
