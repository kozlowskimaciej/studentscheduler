from studsched.app.version import __version__


def test_get_version(test_client):
    response = test_client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_subjects(test_client):
    response = test_client.get("/api/v1/subjects")
    assert response.status_code == 200
    assert response.json() == {"subjects": [{"id": "1", "name": "ZPRP"}]}
