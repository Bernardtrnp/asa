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


def test_account_actived_failed(client):
    response = client.patch(
        "/short.me/auth/account-active/active/abcdefgh",
        json={
            "otp": "123456",
        },
    )
    assert response.status_code == 404
    assert "IS_INVALID" in response.json["errors"]["otp"]
