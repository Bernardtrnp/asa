import nextcord
from nextcord.ext import commands
import yaml
import certifi
import os
from mongoengine import connect, get_connection
from configs import token, mongodb, mongodb_url


if not os.environ.get("SSL_CERT_FILE"):
    os.environ["SSL_CERT_FILE"] = certifi.where()

with open("./configs/config.yaml", "r", encoding="utf8") as f:
    data = yaml.safe_load(f)

connect(
    db=mongodb,
    host=mongodb_url,
)


bot = commands.Bot(
    intents=nextcord.Intents.all(),
    case_insensitive=True,
    default_guild_ids=data["guild_id"],
)

for ext in data["extensions"]:
    bot.load_extension(ext)


try:
    conn = get_connection()
    conn.admin.command("ping")
    print("koneksi MongoDB sukses!")
except Exception as e:
    print(f"koneksi gagal: {e}")
else:
    bot.run(token)
