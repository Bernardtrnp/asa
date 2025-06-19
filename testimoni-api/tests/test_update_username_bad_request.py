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


def test_update_profile_empty_username(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": "",
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_space_username(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": " ",
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_none(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": None,
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_must_text_int(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": 1,
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_must_text_float(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": 0.1,
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_must_text_bool(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": True,
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_must_text_list(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": [True],
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_must_text_tuple(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": (True),
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_too_short(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": "abc",
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "TOO_SHORT" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]


def test_update_profile_username_too_long(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": "abcdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
        },
        headers={
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ1YTkxODI1YjA4NmFiMTcxYzM0ZmIiLCJpYXQiOjE3NDkzOTY1MDV9.E6ES0C09B27lIOt6OCF_RyY3tlQe9zIOpb000lD-38soTkEJ1iEFdu7vJuXVRjp7oAaWY8QMuFiURAlycVgacFRLelE68deTSoPjvYHlLufprED1cPh2pUh_HFEIuKUZXhFSaOPNmTRaGIvlEcpT2ZhfMjh3w0wg0ebbhASIsf5fDIvSMNhJDl20DxhgCwq_fuZdWH_prGeCxOIa2qVw-pBZTTAYVL_PPHk2rcGU6h7eap72KhyUWGDu6T2JK7VP48cUqihcyE4f2aOjiJWroVFNYl7462mFFPb6hC0whJiI-sUY6KX0X7HbT8kbUdhYfllEQH3QaT-rmZOprgeZJQ"
        },
    )
    assert response.status_code == 400
    assert "TOO_LONG" in response.json["errors"]["username"]
    assert "invalid data" in response.json["message"]
