import nextcord
from nextcord.ext import commands
from ui import AddTestimoniUI


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")
        self.bot.add_view(AddTestimoniUI())


def setup(bot):
    bot.add_cog(OnReady(bot))
