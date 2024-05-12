from sqlmodel import Session, SQLModel
from fastapi.testclient import TestClient
import pytest

from studsched.app.application import create_application
from studsched.app.db.session import engine
from studsched.app.db.models import models


@pytest.fixture
def app():
    return create_application()


@pytest.fixture
def test_client(app):
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def db_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.close()
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def linked_course(db_session: Session):
    linked_course = models.LinkedCourse()
    db_session.add(linked_course)
    db_session.commit()
    db_session.refresh(linked_course)
    return linked_course


@pytest.fixture
def requirement(db_session: Session, linked_course: models.LinkedCourse):
    requirement = models.Requirement(
        task_type=models.TaskType.LAB,
        requirement_type=models.RequirementType.TOTAL,
        threshold=5,
        threshold_type=models.ThresholdType.POINTS,
        linked_course_id=linked_course.id,
    )
    db_session.add(requirement)
    db_session.commit()
    return requirement


@pytest.fixture
def filled_db(db_session: Session, linked_course, requirement):
    yield db_session
