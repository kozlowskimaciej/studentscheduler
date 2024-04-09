from studsched.app.version import __version__
from studsched.app.schemas.base import (
    SubjectStatus,
    TaskType,
    RequirementType,
    ThresholdType,
)


def test_get_version(test_client):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_subjects(test_client):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 1

    subject = res[0]
    assert subject["id"] == "1"
    assert subject["name"] == "ZPRP"
    assert subject["status"] == SubjectStatus.PASSED
    assert len(subject["tasks"]) == 1
    assert len(subject["requirements"]) == 1

    task = subject["tasks"][0]
    assert task["max_points"] == 10
    assert task["result"] is None
    assert task["deadline"] == "2002-01-27T01:00:00"
    assert task["task_type"] == TaskType.LAB
    assert not task["ended"]
    assert task["description"] == ""

    requirement = subject["requirements"][0]
    assert requirement["task_type"] == TaskType.LAB
    assert requirement["requirement_type"] == RequirementType.TOTAL
    assert requirement["threshold"] == 5
    assert requirement["threshold_type"] == ThresholdType.POINTS


def test_add_requirements(test_client):
    response = test_client.post(
        "/api/v1/subjects/1/requirements",
        json=[
            {
                "task_type": TaskType.LAB,
                "requirement_type": RequirementType.TOTAL,
                "threshold": 5,
                "threshold_type": ThresholdType.POINTS,
            }
        ],
    )
    assert response.status_code == 200
    res = response.json()

    assert len(res) == 1

    requirement = res[0]
    assert requirement["task_type"] == TaskType.LAB
    assert requirement["requirement_type"] == RequirementType.TOTAL
    assert requirement["threshold"] == 5
    assert requirement["threshold_type"] == ThresholdType.POINTS
