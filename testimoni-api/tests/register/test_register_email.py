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


def test_register_empty_email(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_email_only_spaces(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": " ",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_email_none(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": None,
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_integer_email(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": 1,
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_float_email(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": 0.1,
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_boolean_email(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": True,
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_list_email(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": ["email@example.com"],
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_tuple_email(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": (True),
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_email_too_long(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "dsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "TOO_LONG" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_email_too_short(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "fa@ac",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "TOO_SHORT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_register_email_invalid_format(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "dsdsadsadsadsadsa",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_INVALID" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]
