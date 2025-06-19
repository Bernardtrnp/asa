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


def test_login_empty_password(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_password_only_spaces(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": " ",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_password_none(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": None,
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_integer_password(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": 123456,
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_float_password(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": 12.34,
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_boolean_password(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": True,
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_list_password(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": ["Password123!"],
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_tuple_password(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": ("Password123!",),
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["password"]
    assert "invalid data" == response.json["message"]
