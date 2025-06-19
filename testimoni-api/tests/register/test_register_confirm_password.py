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


def test_register_empty_confirm_password(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_confirm_password_only_spaces(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": " ",
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_confirm_password_none(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": None,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_integer_confirm_password(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": 1,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_float_confirm_password(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": 0.1,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_boolean_confirm_password(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": True,
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_list_confirm_password(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": [True],
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_rejects_tuple_confirm_password(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": (True),
            "password": "Password123!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["confirm_password"]
    assert "invalid data" == response.json["message"]


def test_register_confirm_password_too_long(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "D3v1n@634824!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
            "password": "D3v1n@634824!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "TOO_LONG" in response.json["errors"]["password_security"]
    assert "invalid data" == response.json["message"]


def test_register_confirm_password_too_short(client):
    response = client.post(
        "/short.me/register",
        json={
            "username": "farras",
            "email": "farras.pramudita@gmail.com",
            "confirm_password": "D3v1",
            "password": "D3v1",
            "provider": "auth_internal",
        },
    )
    assert response.status_code == 400
    assert "TOO_SHORT" in response.json["errors"]["password_security"]
    assert "invalid data" == response.json["message"]
