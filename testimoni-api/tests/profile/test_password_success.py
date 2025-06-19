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


def test_me_success(client):
    response = client.patch(
        "/short.me/user/password",
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0ODg0NDN9.eIIY-6qN4gxA51qAYpuPIJUm-JTqT61qNXn6Qp9lOeZAABxqpNGdfTOoXifogMWaTI6L6C0Tf_D7O7FraOZyP9d-9HrKriMhJOngVmAlArslB2zQPfF9uUtx6eh5nQdEYa04gVsXg3uU2vY4C6fXGIwLh3EMR7rX17rNCR2z01Zd5fcXHr06mI9aXJlpymqwmfVmnUVtnMEkuwZT338beIvdEmMO6YECVQ-PLtanKKfDgMB4sUMRdQcFlABXYx20sDWvmigqXZzzkFbMc1Gw1ZptnhZ-UcgXjZakJeCHzmp3Rmn4Ib3U1REexaW48KHoDCLbZfn17g1GisBUEST4Eg"
        },
        json={"password": "F4r4h634824@", "confirm_password": "F4r4h634824@"},
    )
    assert response.status_code == 201
    assert "successfully get user" == response.json["message"]
