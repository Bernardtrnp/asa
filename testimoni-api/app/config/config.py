from dotenv import load_dotenv
import os

load_dotenv()

database_mongodb = os.getenv("DATABASE_MONGODB")
database_mongodb_url = os.getenv("DATABASE_MONGODB_URL")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
webhook_url = os.getenv("WEBHOOK_URL")
webhook_username = os.getenv("WEBHOOK_USERNAME")
celery_url = os.getenv("CELERY_URL")
