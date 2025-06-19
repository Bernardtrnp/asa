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


def test_send_email_empty_email(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": "",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_send_email_spaces_only(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": "   "},
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_none(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": None},
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_integer(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": 123},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_float(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": 1.23},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_boolean(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": True},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_list(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": ["email@example.com"]},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_tuple(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": ("email@example.com",)},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_invalid_format(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": "notanemail"},
    )
    assert response.status_code == 400
    assert "IS_INVALID" in response.json["errors"]["email"]
    assert response.json["message"] == "invalid data"


def test_send_email_not_found(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={"email": "notanemail@gmail.com"},
    )
    assert response.status_code == 404
    assert "NOT_FOUND" in response.json["errors"]["user"]
    assert "email not found" == response.json["message"]
