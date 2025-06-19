from .database import Database
from models import ApiKeyModel


class ApiKeyDatabase(Database):
    @staticmethod
    async def insert(discord_id, api_key):
        if user_data := ApiKeyModel.objects(discord_id=discord_id).first():
            user_data.api_key = api_key
            user_data.save()
            return user_data
        user_data = ApiKeyModel(discord_id=discord_id, api_key=api_key)
        user_data.save()
        return user_data

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def get(category, **kwargs):
        discord_id = kwargs.get("discord_id")
        if category == "by_discord_id":
            return ApiKeyModel.objects(discord_id=discord_id).first()

    @staticmethod
    async def update(category, **kwargs):
        pass
