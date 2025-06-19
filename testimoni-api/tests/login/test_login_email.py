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


def test_login_empty_email(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_email_only_spaces(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": " ",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_email_none(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": None,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_integer_email(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": 1,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_float_email(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": 0.1,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_boolean_email(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": True,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_list_email(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": ["email@example.com"],
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_tuple_email(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": (True,),
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_login_email_invalid_format(client):
    response = client.post(
        "/short.me/register",
        json={
            "email": "anbcd",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_INVALID" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]
