from flask import jsonify, request, make_response
from ..utils import generate_etag


class ApiKeyController:
    @staticmethod
    async def user_api_key(user, api_key):
        current_data = {
            "id": f"{user.id}",
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "avatar": user.avatar,
            "api_key": api_key,
        }
        etag = generate_etag(current_data)
        client_etag = request.headers.get("If-None-Match")
        if client_etag == etag:
            return make_response("", 304)

        response_data = {
            "data": current_data,
            "message": "success get current user",
        }

        response = make_response(jsonify(response_data), 200)
        response.headers["Content-Type"] = "application/json"
        response.headers["ETag"] = etag
        return response
