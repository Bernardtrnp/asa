import pytest
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


def test_status_email_failed(client):
    response = client.get(
        "/short.me/auth/account-active/verify/abcd",
    )
    assert response.status_code == 404
    assert "IS_INVALID" in response.json["errors"]["token"]
    assert "token invalid" == response.json["message"]
