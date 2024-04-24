from fastapi.testclient import TestClient
from sqlmodel import Session
from fastapi import FastAPI, status

from studsched.app.api.base import get_db
from studsched.app.version import __version__
from studsched.app.db.models import models


def test_get_version(test_client: TestClient):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_get_subjects_empty(test_client: TestClient):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 0


def test_get_subjects(app, test_client: TestClient, filled_db: Session):
    app.dependency_overrides[get_db] = lambda: filled_db

    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 1

    subject = res[0]
    assert subject["id"] == 1
    assert subject["name"] == "Subject"
    assert subject["status"] == models.SubjectStatus.IN_PROGRESS
    assert len(subject["requirements"]) == 1

    requirement = subject["requirements"][0]
    assert requirement["task_type"] == models.TaskType.LAB
    assert requirement["requirement_type"] == models.RequirementType.TOTAL
    assert requirement["threshold"] == 5
    assert requirement["threshold_type"] == models.ThresholdType.POINTS


def test_replace_requirements(
    app: FastAPI,
    test_client: TestClient,
    filled_db: Session,
    linked_course: models.LinkedCourse,
    requirement: models.Requirement,
):
    app.dependency_overrides[get_db] = lambda: filled_db

    subjects = test_client.get("/api/v1/subjects").json()
    requirements = subjects[0]["requirements"]
    assert len(requirements) == 1

    requirement_update = models.RequirementCreate(**requirement.model_dump())
    res = test_client.put(
        f"/api/v1/subjects/{linked_course.id}/requirements",
        json=[requirement_update.model_dump()] * 2,
    )
    assert res.status_code == status.HTTP_200_OK

    subjects = test_client.get("/api/v1/subjects").json()
    requirements = subjects[0]["requirements"]
    assert len(requirements) == 2

    for requirement in requirements:
        assert requirement["task_type"] == models.TaskType.LAB
        assert requirement["requirement_type"] == models.RequirementType.TOTAL
        assert requirement["threshold"] == 5
        assert requirement["threshold_type"] == models.ThresholdType.POINTS
