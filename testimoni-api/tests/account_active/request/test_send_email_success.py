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


def test_send_email_success(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": "bigis22929@adrewire.com",
        },
    )
    assert response.status_code == 201
    assert "successfully send account active email" == response.json["message"]
