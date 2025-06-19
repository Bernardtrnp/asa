from .database import Database
from ..models import UserModel


class UserDatabase(Database):
    @staticmethod
    async def insert(avatar, username, discord_id, email, is_active, created_at):
        if user_data := UserModel.objects(
            email=email.lower(), discord_id=discord_id
        ).first():
            if user_data.avatar != avatar:
                user_data.avatar = avatar
            if not user_data.email:
                user_data.email = email
            user_data.is_active = is_active
            user_data.save()
            return user_data
        user_data = UserModel(
            username=username,
            email=email,
            created_at=created_at,
            updated_at=created_at,
            avatar=avatar,
            discord_id=discord_id,
        )
        await user_data.unique_field()
        user_data.is_active = is_active
        user_data.save()
        return user_data

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def update(category, **kwargs):
        pass

    @staticmethod
    async def get(category, **kwargs):
        pass
