from fastapi.testclient import TestClient

from studsched.app.version import __version__


def test_get_version(test_client: TestClient):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}
