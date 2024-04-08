from studsched.app.version import __version__
from studsched.app.schemas.base import SubjectStatus


def test_get_version(test_client):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_subjects(test_client):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1",
            "name": "ZPRP",
            "status": SubjectStatus.PASSED,
            "tasks": [],
        }
    ]
