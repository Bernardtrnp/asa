from flask import jsonify
from ..config import client_id, client_secret, redirect_uri
import requests
from ..databases import UserDatabase, BlacklistTokenDatabase
from ..utils import AuthJwt, generate_api_key


class LoginController:
    @staticmethod
    async def user_logout(user, token):
        if not (
            user_token := await BlacklistTokenDatabase.insert(user.id, token["iat"])
        ):
            return (
                jsonify(
                    {
                        "message": "invalid or expired token",
                        "errors": {"token": ["IS_INVALID"]},
                    }
                ),
                401,
            )
        return jsonify({"message": "successfully logout"}), 201

    @staticmethod
    async def user_login(code, timestamp):
        created_at = int(timestamp.timestamp())
        errors = {}
        if code is None or (isinstance(code, str) and code.strip() == ""):
            errors.setdefault("code", []).append("IS_REQUIRED")
        else:
            if not isinstance(code, str):
                errors.setdefault("code", []).append("MUST_TEXT")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response_token = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data=data,
            headers=headers,
            auth=(client_id, client_secret),
        )
        resp_token = response_token.json()
        if "error" in resp_token:
            return (
                jsonify(
                    {"errors": {"code": ["IS_INVALID"]}, "message": "invalid code"}
                ),
                401,
            )
        response_current_user = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": f"Bearer {resp_token['access_token']}"},
        )
        resp_current_user = response_current_user.json()
        result_user = await UserDatabase.insert(
            f'https://cdn.discordapp.com/avatars/{resp_current_user['id']}/{resp_current_user["avatar"]}.png',
            resp_current_user["username"],
            resp_current_user["id"],
            resp_current_user["email"],
            resp_current_user["verified"],
            created_at,
        )
        access_token = await AuthJwt.generate_jwt(f"{result_user.id}", created_at)
        return (
            jsonify(
                {
                    "message": "user login successfully",
                    "data": {
                        "id": f"{result_user.id}",
                        "username": result_user.username,
                        "created_at": result_user.created_at,
                        "updated_at": result_user.updated_at,
                        "is_active": result_user.is_active,
                        "email": result_user.email,
                    },
                    "token": {
                        "access_token": access_token,
                    },
                }
            ),
            201,
        )
