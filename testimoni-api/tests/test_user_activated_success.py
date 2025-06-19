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


def test_account_actived_success(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0NWE5MTgyNWIwODZhYjE3MWMzNGZiIiwiY3JlYXRlZF9hdCI6MTc0OTM5NTczNn0.um9JzHMthYT-VoHiWJGII8W4dd8",
        json={
            "otp": "XBSWQF",
        },
    )
    assert response.status_code == 201
    assert "successfully verify user account" == response.json["message"]
