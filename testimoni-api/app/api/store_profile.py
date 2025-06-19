from flask import Blueprint
from ..controllers import StoreProfileController

store_profile_router = Blueprint("store_profile_router", __name__)


@store_profile_router.get("/rakit-app/store/profile")
async def store_profile():
    return await StoreProfileController.store_profile()
