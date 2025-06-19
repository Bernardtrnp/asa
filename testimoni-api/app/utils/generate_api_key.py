import secrets
import uuid


async def generate_api_key():
    prefix = "api_"
    random_part = secrets.token_urlsafe(16)
    uuid_part = uuid.uuid4().hex
    return f"{prefix}{random_part}{uuid_part}"
