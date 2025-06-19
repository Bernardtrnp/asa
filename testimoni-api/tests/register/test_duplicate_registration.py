import pytest
from mongoengine.connection import disconnect
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


def test_duplicate_registration(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "jordimepsu",
            "email": "jordimepsu@gufum.com",
            "confirm_password": "D3v1n@634824",
            "password": "D3v1n@634824",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 409
    assert "the user already exists" == response.json["message"]
    assert "ALREADY_EXISTS" in response.json["errors"]["user"]
