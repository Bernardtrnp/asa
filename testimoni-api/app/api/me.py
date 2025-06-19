from flask import Blueprint, request
from ..utils import jwt_required
from ..controllers import MeController
from .. import limiter

me_router = Blueprint("me_router", __name__)


@me_router.get("/rakit-app/user/@me")
@limiter.limit("60 per minute")
@jwt_required()
async def user_me():
    user = request.user
    return await MeController.user_me(user)
