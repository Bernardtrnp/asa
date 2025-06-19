import nextcord
from nextcord.ext import commands, application_checks
from utils import (
    InteractionResponse,
)
import yaml


class OnApplicationCommandError(commands.Cog):
    with open("./configs/config.yaml", "r", encoding="utf8") as f:
        data = yaml.safe_load(f)

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction, error):
        error = getattr(error, "original", error)
        if isinstance(error, application_checks.ApplicationMissingAnyRole):
            return await interaction.send(
                embed=nextcord.Embed(
                    description=f"""{self.data["emoji_cross"]} failed process your transaction
-# you don't have permission""",
                    color=nextcord.Color.red(),
                ),
                ephemeral=True,
            )
        else:
            raise error


def setup(bot):
    bot.add_cog(OnApplicationCommandError(bot))
