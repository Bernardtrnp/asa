import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_login_success(client):
    response = client.get(
        "/rakit-app/user/@me",
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODRkMTFlODE2ODlkYWY0NzBhMTNmOGQiLCJpYXQiOjE3NDk4ODU0OTl9.sL1zPVPChvDYcm3SE4iD5Q4PlnCZydaDjyhqqw74ioG8UrVlwcVSBaqNVCxZVCn4VVVMf9teN6OajJrc1OVeV76o-uZKjlOGfrIkE8fH29U1P8geniYX7j7tCZk6O1-cIhElkeW5rLARP3MpzQrfNlsJ1lBZEdtiHsHZ-X90xeRjpStvXB0TKDGOTP5Usz3fbo1IxxQDrLWB8qs2y78-f15U69MRTtFqDaO_BaWr1ChbXG__tS1a7_izaFmObUgvdN2qXANH8FsJ7Rj3_H59nxJApCznO5g8uD3x45FoVQQ9MH0od6Qsnsm4JYio8NZZT0OjtCA48FyecgG9MRw9ag"
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "success get current user"
