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


def test_reset_password_confirm_password_empty(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": "Password123!",
            "confirm_password": "",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["confirm_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_confirm_password_only_spaces(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": "Password123!",
            "confirm_password": " ",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["confirm_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_confirm_password_none(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": "Password123!",
            "confirm_password": None,
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["confirm_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_confirm_password_mismatch(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": "Password123!",
            "confirm_password": "Password321!",
        },
    )
    assert response.status_code == 400
    assert "IS_MISMATCH" in response.json["errors"]["password_match"]
    assert response.json["message"] == "invalid data"


def test_reset_password_confirm_password_not_string(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": "Password123!",
            "confirm_password": True,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["confirm_password"]
    assert response.json["message"] == "invalid data"
