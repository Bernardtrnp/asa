import pytest
from app import create_app


@pytest.fixture()
def app():
    test_config = {
        "MONGODB_SETTINGS": {
            "db": "test_db",
            "host": "mongodb://localhost:27018",
            "connect": False,
        },
    }
    app = create_app(test_config)
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_login_success(client):
    response = client.post(
        "/rakit-app/auth/login",
        json={
            "code": "BlPmrQCMOQApp3oriujSyQIdBzftks",
        },
    )
    assert response.status_code == 201
    assert response.json["message"] == "user login successfully"
    print(response.json)
