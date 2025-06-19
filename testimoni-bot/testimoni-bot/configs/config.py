from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")
mongodb = os.getenv("MONGODB")
mongodb_url = os.getenv("MONGODB_URL")
