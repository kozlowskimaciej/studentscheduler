from sqlmodel import Session, select
from studsched.app.db.queries.queries import get_subjects, update_requirement
from studsched.app.db.models import models
import pytest
from sqlalchemy.orm.exc import NoResultFound


def test_get_subjects_empty(db_session: Session):
    res = get_subjects(db_session)
    assert res == []


def test_get_subjects(filled_db: Session):
    res = get_subjects(filled_db)
    assert len(res) == 1


def test_update_requirement(filled_db: Session):
    requirement = filled_db.exec(select(models.Requirement)).one()
    fields_dict = requirement.model_dump()
    assert requirement.threshold == 5

    fields_dict["threshold"] = 10
    updated_requirement = models.RequirementUpdate(**fields_dict)
    update_requirement(filled_db, requirement.id, updated_requirement)

    requirement = filled_db.exec(select(models.Requirement)).one()
    assert requirement.threshold == 10


def test_update_nonexistent_requirement(db_session: Session):
    requirement = models.RequirementUpdate(
        task_type=models.TaskType.LAB,
        requirement_type=models.RequirementType.TOTAL,
        threshold=5,
        threshold_type=models.ThresholdType.POINTS,
        linked_course_id=1,
    )

    nonexistent_id = 423432
    found = db_session.get(models.Requirement, nonexistent_id)
    assert found is None

    with pytest.raises(NoResultFound):
        update_requirement(db_session, nonexistent_id, requirement)
