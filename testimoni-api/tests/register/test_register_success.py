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
    response = client.post(
        "/short.me/register",
        json={
            "username": "bigis22929",
            "email": "bigis22929@adrewire.com",
            "confirm_password": "D3v1n@634824",
            "password": "D3v1n@634824",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 201
    assert "user registered successfully" == response.json["message"]
