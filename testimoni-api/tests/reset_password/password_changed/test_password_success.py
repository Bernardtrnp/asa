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


def test_register_success(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NjI3N30.SR7KMkucrpxNQpALc55PqA1M2aI",
        json={
            "confirm_password": "F4r@h634824",
            "new_password": "F4r@h634824",
        },
    )
    assert response.status_code == 201
    assert "successfully reset password" == response.json["message"]
