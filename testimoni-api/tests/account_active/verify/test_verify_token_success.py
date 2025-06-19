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


def test_status_email_success(client):
    response = client.get(
        "/short.me/auth/account-active/verify/eyJ1c2VyX2lkIjoiNjg0ODJiYWI5ZWYwNDViZjA5N2EwMTMyIiwiY3JlYXRlZF9hdCI6MTc0OTU2MDI5MH0.7z7bcV5k9eA9zkg9cPJvlcfxCWs",
    )
    assert response.status_code == 200
    assert "successfully get account active information" == response.json["message"]
