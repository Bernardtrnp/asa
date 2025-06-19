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


def test_me_failed(client):
    response = client.get(
        "/short.me/@me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzA0NDd9.Mekc7ffLY0uiaL1S7jU6sY-8ILsVgMClonX1_6GTeuhzGG0neRaksMoJ3woyo95tjTqlkUPhTU22rkKhZKOYqNVhA-DRm8R68Vs5SA_IaUvfXifHRpkwUWND2Jd0AAwXBwthsKyBm0vXUa_TFB0fR0G9JN3uJDPBaPdkjV7HBnzoZ7IRW53msnzr2bqo4u23LNzayQz_Dso75l6vTZn9D_TNq5OpX8XgL1fgZJ4nXdjYv-aAv5VVo4w57vT694D9pv6Or9ASuazNOYViK1m4AYC9StoW2QOr1K7xyebPqL-4JgbkiKM0E_dN7jXxTz2ONwXggw4R-Stpff8SkfNmOw"
        },
    )
    assert response.status_code == 401
    assert "invalid or expired token" == response.json["message"]
