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


def test_profile_update_empty_username(client):
    response = client.patch(
        "/short.me/user/username",
        json={
            "username": "",
        },
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "invalid data" == response.json["message"]
    assert "IS_REQUIRED" in response.json["errors"]["username"]


def test_profile_update_username_spaces_only(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": "   "},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_none(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": None},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "IS_REQUIRED" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_integer(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": 123},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_float(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": 12.34},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_boolean(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": False},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_list(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": ["abc"]},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_tuple(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": ("abc",)},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "MUST_TEXT" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_too_long(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": "a" * 100},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "TOO_LONG" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"


def test_profile_update_username_too_short(client):
    response = client.patch(
        "/short.me/user/username",
        json={"username": "abc"},
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODQ2Y2MwMTZhM2U3MmFjNjViZGU1YjEiLCJpYXQiOjE3NDk0NzM1MDl9.fpZQd-9lq3fTifAZI3s_3Ppmgpg3cMLKN77wMTiLfWVgMxoPiYneysAutvZbNYcd5e1cdb6lGY_ubmoAlz0xGgbqZEUSENIHWh9-7iqrpGSB8Unhh4Iztk04YMjwAw8OWYOtm3gdUsgbsxeRO5fk9J3qYy_ZGcYoREETqpJn9X6Rc-wSji_n8qtuUXVRFytIWh_eDi2WfliyX_2S03c9egAMT21Y6FIU0RCQOuwOKNa8LCZsXa9XhXMSg9GV21yr_YEKBaA_Yiib6aMPYAutrtYLTyF6IcP6ntHrRKOwKUTodia6icTRECmCvvuQjveLxLSd6OscjX8cOr6o-d4Wkw"
        },
    )
    assert response.status_code == 400
    assert "TOO_SHORT" in response.json["errors"]["username"]
    assert response.json["message"] == "invalid data"
