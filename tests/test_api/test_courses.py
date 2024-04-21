from fastapi.testclient import TestClient
from sqlmodel import Session

from studsched.app.api.base import get_db
from studsched.app.db.models.models import (
    CourseStatus,
    TaskType,
    RequirementType,
    ThresholdType,
)


def test_courses_empty(test_client: TestClient):
    response = test_client.get("/api/v1/courses")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 0


def test_courses(app, test_client: TestClient, filled_db: Session):
    app.dependency_overrides[get_db] = lambda: filled_db

    response = test_client.get("/api/v1/courses")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 1

    course = res[0]
    assert course["id"] == 1
    assert course["name"] == "Course"
    assert course["status"] == CourseStatus.IN_PROGRESS
    assert len(course["requirements"]) == 1

    requirement = course["requirements"][0]
    assert requirement["task_type"] == TaskType.LAB
    assert requirement["requirement_type"] == RequirementType.TOTAL
    assert requirement["threshold"] == 5
    assert requirement["threshold_type"] == ThresholdType.POINTS


def test_add_requirements(app, test_client: TestClient, filled_db: Session):
    app.dependency_overrides[get_db] = lambda: filled_db

    response = test_client.post(
        "/api/v1/courses/requirements/1",
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

    response = test_client.get("/api/v1/courses")
    assert response.status_code == 200
    res = response.json()

    assert len(res) == 1
    course = res[0]
    assert len(course["requirements"]) == 2

    requirement = course["requirements"][1]
    assert requirement["task_type"] == TaskType.EXAM
    assert requirement["requirement_type"] == RequirementType.SEPARATELY
    assert requirement["threshold"] == 50
    assert requirement["threshold_type"] == ThresholdType.PERCENT
    assert requirement["id"]
