from flask import Blueprint, request
from ..controllers import LoginController
from ..utils import jwt_required

login_router = Blueprint("login_router", __name__)


@login_router.post("/rakit-app/auth/login")
async def user_login():
    data = request.json
    timestamp = request.timestamp
    code = data.get("code", "")
    return await LoginController.user_login(code, timestamp)


@login_router.post("/rakit-app/auth/logout")
@jwt_required()
async def user_logout():
    user = request.user
    token = request.token
    return await LoginController.user_logout(user, token)
