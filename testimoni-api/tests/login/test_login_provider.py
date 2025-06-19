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


def test_login_empty_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": "",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_provider_only_spaces(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": " ",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_provider_none(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": None,
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_integer_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": 1,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_float_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": 0.5,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_boolean_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": True,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_list_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": ["auth_internal"],
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_tuple_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": ("auth_internal",),
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_invalid_provider(client):
    response = client.post(
        "/short.me/login",
        json={
            "email": "email@example.com",
            "password": "Password123!",
            "provider": "abcd",
        },
    )
    assert response.status_code == 400
    assert "IS_INVALID" in response.json["errors"]["provider"]
    assert "invalid data" == response.json["message"]


def test_login_rejects_invalid_token(client):
    response = client.post(
        "/short.me/login",
        json={
            "provider": "google",
            "token": "abcd",
        },
    )
    assert response.status_code == 400
    assert "IS_INVALID" in response.json["errors"]["token"]
    assert "invalid data" == response.json["message"]
