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


def test_activation_success(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODJiYWI5ZWYwNDViZjA5N2EwMTMyIiwiY3JlYXRlZF9hdCI6MTc0OTU2MDY0NH0.C3nJm5fEMjP8OZc5X528Pd2xw_0",
        json={"otp": "MBNOZB"},
    )
    assert response.status_code == 201
    assert "successfully verify user account" == response.json["message"]
