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


def test_activation_empty_otp(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": ""},
    )
    assert response.status_code == 400
    assert "invalid data" == response.json["message"]
    assert "IS_REQUIRED" in response.json["errors"]["otp"]


def test_activation_otp_spaces_only(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": "   "},
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"


def test_activation_otp_none(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": None},
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"


def test_activation_otp_integer(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": 123456},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"


def test_activation_otp_float(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": 123.45},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"


def test_activation_otp_boolean(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": True},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"


def test_activation_otp_list(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": ["123456"]},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"


def test_activation_otp_tuple(client):
    response = client.patch(
        "/short.me/auth/account-active/active/eyJ1c2VyX2lkIjoiNjg0ODZiNDBlNzkyZDkyMWZhNThhNDYyIiwiY3JlYXRlZF9hdCI6MTc0OTU3NzQ0OH0.Pb-CtW-BS4a2cGZn_c_cZNgvSTc",
        json={"otp": ("123456",)},
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["otp"]
    assert response.json["message"] == "invalid data"
