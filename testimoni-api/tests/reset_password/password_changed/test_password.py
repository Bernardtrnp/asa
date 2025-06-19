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


def test_reset_password_empty_password(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": "",
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_password_only_spaces(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": " ",
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_password_none(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": None,
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_rejects_integer_password(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": 1,
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_rejects_float_password(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": 0.1,
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_rejects_boolean_password(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": True,
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_rejects_list_password(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": [True],
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_rejects_tuple_password(client):
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": (True,),
            "confirm_password": "Password123!",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["new_password"]
    assert response.json["message"] == "invalid data"


def test_reset_password_password_too_long(client):
    long_pw = "D3v1n@634824" + "!" * 100
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": long_pw,
            "confirm_password": long_pw,
        },
    )
    assert response.status_code == 400
    assert "TOO_LONG" in response.json["errors"]["password_security"]
    assert response.json["message"] == "invalid data"


def test_reset_password_password_too_short(client):
    short_pw = "D3v1"
    response = client.patch(
        "/short.me/auth/reset-password/confirm/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU4NDc3NX0.VMU1mDSwXPuNkwlVAXXjj3WwdzU",
        json={
            "new_password": short_pw,
            "confirm_password": short_pw,
        },
    )
    assert response.status_code == 400
    assert "TOO_SHORT" in response.json["errors"]["password_security"]
    assert response.json["message"] == "invalid data"
