import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_account_active_empety_email(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": "",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_space_email(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": " ",
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_email_none(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": None,
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_required_invalid_email(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": "abcde",
        },
    )
    assert response.status_code == 400
    assert "IS_INVALID" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_required_email_not_found(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": "andanafarras@gmail.com",
        },
    )
    assert response.status_code == 404
    assert "NOT_FOUND" in response.json["errors"]["user"]
    assert "email not found" in response.json["message"]


def test_account_active_must_text_int(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": 1,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_must_text_float(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": 1.1,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_must_text_bool(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": True,
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_must_text_tuple(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": (1),
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]


def test_account_active_must_text_list(client):
    response = client.post(
        "/short.me/auth/account-active/request",
        json={
            "email": [1],
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["email"]
    assert "invalid data" == response.json["message"]
