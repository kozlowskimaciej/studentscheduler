from fastapi.testclient import TestClient
from fastapi import FastAPI, status
from sqlmodel import Session
import pytest

from studsched.app.api.base import get_db, get_current_user
from studsched.app.version import __version__
from studsched.app.db.models import models


@pytest.fixture
def mock_current_user(
    app: FastAPI,
    user: models.User,
):
    app.dependency_overrides[get_current_user] = lambda: user


@pytest.fixture
def mock_db_with_user(
    app: FastAPI,
    db_with_user: Session,
):
    app.dependency_overrides[get_db] = lambda: db_with_user


@pytest.fixture
def mock_db_with_courses(
    app: FastAPI,
    db_with_courses: Session,
):
    app.dependency_overrides[get_db] = lambda: db_with_courses


def test_get_version(test_client: TestClient):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


@pytest.mark.usefixtures("mock_db_with_user", "mock_current_user")
def test_get_subjects_empty(
    test_client: TestClient,
):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 0


@pytest.mark.usefixtures("mock_db_with_courses", "mock_current_user")
def test_get_subjects(
    test_client: TestClient,
):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 1

    subject = res[0]
    assert subject["id"] == 1
    assert subject["name"] == "Zaawansowane Programowanie w Pythonie"
    assert subject["status"] == models.SubjectStatus.IN_PROGRESS
    assert len(subject["requirements"]) == 1

    requirement = subject["requirements"][0]
    assert requirement["task_type"] == models.TaskType.LAB
    assert requirement["requirement_type"] == models.RequirementType.TOTAL
    assert requirement["threshold"] == 5
    assert requirement["threshold_type"] == models.ThresholdType.POINTS


@pytest.mark.usefixtures("mock_db_with_courses")
def test_get_subjects_no_current_user(
    test_client: TestClient,
):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("mock_db_with_courses", "mock_current_user")
def test_add_requirements(
    test_client: TestClient,
):

    response = test_client.post(
        "/api/v1/subjects/1/requirements",
        json=[
            {
                "task_type": models.TaskType.EXAM,
                "requirement_type": models.RequirementType.SEPARATELY,
                "threshold": 50,
                "threshold_type": models.ThresholdType.PERCENT,
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
    assert requirement["task_type"] == models.TaskType.EXAM
    assert requirement["requirement_type"] == models.RequirementType.SEPARATELY
    assert requirement["threshold"] == 50
    assert requirement["threshold_type"] == models.ThresholdType.PERCENT
    assert requirement["id"]
