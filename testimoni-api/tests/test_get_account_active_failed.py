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


def test_get_account_active_not_found(client):
    response = client.get(
        "/short.me/auth/account-active/status/abcdefgh",
    )
    assert response.status_code == 404
    assert "IS_INVALID" in response.json["errors"]["token"]
    assert "token invalid" == response.json["message"]


def test_get_account_active_verify_not_found(client):
    response = client.get(
        "/short.me/auth/account-active/verify/abcdefgh",
    )
    assert response.status_code == 404
    assert "IS_INVALID" in response.json["errors"]["token"]
    assert "token invalid" == response.json["message"]
