from .database import Database
from ..models import TestimoniModel, UserModel


class TestimoniDatabase(Database):
    @staticmethod
    async def insert(discord_id, rating, description, url_testimoni, created_at):
        if user_data := UserModel.objects(discord_id=discord_id).first():
            testimoni_data = TestimoniModel(
                rating=rating,
                description=description,
                url_testimoni=url_testimoni,
                created_at=created_at,
                user=user_data,
            )
            testimoni_data.save()
            return testimoni_data

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        discord_id = kwargs.get("discord_id")
        avatar = kwargs.get("avatar")
        created_at = kwargs.get("created_at")
        rating = kwargs.get("rating")
        description = kwargs.get("description")
        url_testimoni = kwargs.get("url_testimoni")
        username = kwargs.get("username")
        if category == "add_testimoni_by_discord_bot":
            if user_data := UserModel.objects(discord_id=discord_id).first():
                if user_data.avatar != avatar:
                    user_data.avatar = avatar
                user_data.is_active = True
                user_data.save()
            else:
                user_data = UserModel(
                    username=username,
                    created_at=created_at,
                    updated_at=created_at,
                    avatar=avatar,
                    discord_id=discord_id,
                )
                user_data.save()
            testimoni_data = TestimoniModel(
                rating=rating,
                description=description,
                url_testimoni=url_testimoni,
                created_at=created_at,
                user=user_data,
            )
            testimoni_data.save()
            return testimoni_data

    @staticmethod
    async def get(category, **kwargs):
        limit = kwargs.get("limit")
        if category == "all_testimoni":
            return TestimoniModel.objects().order_by("-created_at").limit(limit)
