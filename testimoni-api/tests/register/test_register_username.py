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


def test_register_empty_username(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_username_only_spaces(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": " ",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_username_none(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": None,
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_integer_username(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": 1,
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_float_username(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": 0.1,
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_boolean_username(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": True,
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_list_username(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": [True],
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_tuple_username(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": (True),
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_username_too_long(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "abcdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "TOO_LONG" in response.json["errors"]["username"]
    assert "invalid data" == response.json["message"]


def test_register_username_too_short(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "abcd",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "Password123!",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "invalid data" == response.json["message"]
    assert "TOO_SHORT" in response.json["errors"]["username"]
