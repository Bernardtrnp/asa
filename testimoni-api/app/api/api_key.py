from flask import Blueprint, request
from ..controllers import TestimoniController


api_key_router = Blueprint("api_key_router", __name__)


@api_key_router.post("/rakit-app/user/testimoni")
async def add_testimoni():
    timestamp = request.timestamp
    files = request.files
    form = request.form
    rating = form.get("rating", "")
    description = form.get("description", "")
    discord_id = form.get("discord_id", "")
    username = form.get("username", "")
    avatar = form.get("avatar", "")
    proof = files.get("proof", "")
    return await TestimoniController.add_testimoni(
        rating,
        description,
        proof,
        timestamp,
        "discord_bot",
        discord_id=discord_id,
        username=username,
        avatar=avatar,
        is_active=True,
    )
