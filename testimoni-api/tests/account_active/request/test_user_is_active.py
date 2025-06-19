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


def test_user_is_active(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": "pirtagalta@gufum.com",
        },
    )
    assert response.status_code == 409
    assert "your account is active" == response.json["message"]
    assert "IS_ACTIVE" in response.json["errors"]["user"]
