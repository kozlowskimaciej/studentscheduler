from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import pytest

from studsched.app.application import create_application
from studsched.app.db.session import engine, SessionLocal
from studsched.app.db.base import Base
from studsched.app.db.models import models
from studsched.app.schemas import base as schemas

@pytest.fixture
def app():
    return create_application()


@pytest.fixture
def test_client(app):
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def filled_db(db_session: Session):
    linked_course = models.LinkedCourse()
    db_session.add(linked_course)
    db_session.commit()
    db_session.refresh(linked_course)

    requirement = models.Requirement(
        task_type=schemas.TaskType.LAB,
        requirement_type=schemas.RequirementType.TOTAL,
        threshold=5,
        threshold_type=schemas.ThresholdType.POINTS,
        linked_course_id=linked_course.id,
    )
    db_session.add(requirement)
    db_session.commit()
    yield db_session
