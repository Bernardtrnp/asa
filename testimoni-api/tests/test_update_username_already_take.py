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


def test_update_username_already_take(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": "farrass",
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 409
    assert "successfully update username" in response.json["message"]
