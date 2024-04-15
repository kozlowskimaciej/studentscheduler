from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# from studsched.main import create_application
from studsched.app.api.base import get_db
from studsched.app.version import __version__
from studsched.app.db.models.models import (
    SubjectStatus,
    TaskType,
    RequirementType,
    ThresholdType,
)


def test_get_version(test_client: TestClient):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_subjects_empty(test_client: TestClient):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 0


def test_subjects(app, test_client: TestClient, filled_db: Session):
    app.dependency_overrides[get_db] = lambda: filled_db

    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 1

    subject = res[0]
    assert subject["id"] == 1
    assert subject["name"] == "Subject"
    assert subject["status"] == SubjectStatus.IN_PROGRESS
    assert len(subject["requirements"]) == 1

    requirement = subject["requirements"][0]
    assert requirement["task_type"] == TaskType.LAB
    assert requirement["requirement_type"] == RequirementType.TOTAL
    assert requirement["threshold"] == 5
    assert requirement["threshold_type"] == ThresholdType.POINTS


def test_add_requirements(app, test_client: TestClient, filled_db: Session):
    app.dependency_overrides[get_db] = lambda: filled_db

    response = test_client.post(
        "/api/v1/subjects/1/requirements",
        json=[
            {
                "task_type": TaskType.EXAM,
                "requirement_type": RequirementType.SEPARATELY,
                "threshold": 50,
                "threshold_type": ThresholdType.PERCENT,
            }
        ],
    )
    assert response.status_code == 200

    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()

    assert len(res) == 1
    subject = res[0]
    assert len(subject["requirements"]) == 2

    requirement = subject["requirements"][1]
    assert requirement["task_type"] == TaskType.EXAM
    assert requirement["requirement_type"] == RequirementType.SEPARATELY
    assert requirement["threshold"] == 50
    assert requirement["threshold_type"] == ThresholdType.PERCENT
    assert requirement["id"]
