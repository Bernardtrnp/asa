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


def test_activation_not_found(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NjUxMn0.wrZqjONYl8VwG0sqF7IoyHlRiSo",
        json={"otp": "MBNOZB"},
    )
    assert response.status_code == 404
    assert "token invalid" == response.json["message"]
