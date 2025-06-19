from flask import Blueprint, request
from ..utils import jwt_required
from ..controllers import TestimoniController
from .. import limiter

testimoni_router = Blueprint("testimoni_router", __name__)


@testimoni_router.post("/rakit-app/testimoni")
@jwt_required()
async def add_testimoni():
    timestamp = request.timestamp
    user = request.user
    files = request.files
    form = request.form
    rating = form.get("rating", "")
    description = form.get("description", "")
    proof = files.get("proof", "")
    return await TestimoniController.add_testimoni(
        rating, description, proof, timestamp, "login", user=user
    )


@testimoni_router.get("/rakit-app/testimoni")
@limiter.limit("1 per second")
async def get_all_testimoni():
    params = request.args
    limit = params.get("limit", None)
    per_page = params.get("per_page", "5")
    current_page = params.get("current_page", "1")
    return await TestimoniController.get_all_testimoni(limit, per_page, current_page)
