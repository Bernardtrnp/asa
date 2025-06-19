import nextcord
from nextcord.ext import commands, application_checks
from utils import InteractionResponse
from databases import ApiKeyDatabase
import yaml
import aiohttp
from ui import AddTestimoniUI


class Set(commands.Cog):
    with open("./configs/config.yaml", "r", encoding="utf8") as file:
        data_content = yaml.safe_load(file)

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="set",
        description="for set commands",
    )
    async def set_command(self, interaction: nextcord.Interaction):
        pass

    @set_command.subcommand(
        description="to set button testimoni", inherit_hooks=True, name="button"
    )
    @application_checks.has_any_role(*data_content["role_admin"])
    async def set_button(self, interaction: nextcord.Interaction):
        await InteractionResponse.response_loading(interaction)
        view = AddTestimoniUI()
        await interaction.channel.send(
            embed=nextcord.Embed(
                title="Beri Testimoni",
                description="Untuk beri testimoni, klik tombol dibawah ini",
                color=nextcord.Color.green(),
            ),
            view=view,
        )
        await InteractionResponse.response_success(
            interaction,
            message="success set button testimoni",
            emoji=InteractionResponse.data["emoji_tick"],
        )

    @set_command.subcommand(
        description="to set api key", inherit_hooks=True, name="api-key"
    )
    async def set_api_key(
        self,
        interaction: nextcord.Interaction,
        api_key: str = nextcord.SlashOption(
            name="api-key",
            description="Your API key",
            required=True,
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        url = "http://localhost:5000/rakit-app/user/api-key"
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                resp = await response.json()
                if response.status != 200:
                    return await InteractionResponse.response_error(
                        interaction,
                        message="set api key",
                        emoji=InteractionResponse.data["emoji_cross"],
                        error=resp["message"],
                    )
                await ApiKeyDatabase.insert(interaction.user.id, api_key)
                await InteractionResponse.response_success(
                    interaction,
                    message="success set api key",
                    emoji=InteractionResponse.data["emoji_tick"],
                )

    @nextcord.slash_command(
        name="add-vouch",
        description="for add vouch",
    )
    async def add_vouch(
        self,
        interaction: nextcord.Interaction,
        rating: str = nextcord.SlashOption(
            name="rating",
            description="Your rating",
            required=True,
            choices={
                "⭐": "1",
                "⭐⭐": "2",
                "⭐⭐⭐": "3",
                "⭐⭐⭐⭐": "4",
                "⭐⭐⭐⭐⭐": "5",
            },
        ),
        description: str = nextcord.SlashOption(
            name="description",
            description="Your description",
            required=True,
        ),
        proof: nextcord.Attachment = nextcord.SlashOption(
            name="proof",
            description="Your proof",
            required=False,
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if proof:
            proof_bytes = await proof.read()

        url = "http://localhost:5000/rakit-app/user/testimoni"
        form = aiohttp.FormData()
        form.add_field("rating", f"{rating}")
        form.add_field("description", description)
        form.add_field("discord_id", f"{interaction.user.id}")
        form.add_field("username", f"{interaction.user.name}")
        form.add_field("avatar", f"{interaction.user.avatar}")
        if proof:
            form.add_field(
                "proof",
                proof_bytes,
                filename=proof.filename,
                content_type=proof.content_type or "application/octet-stream",
            )

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form) as response:
                resp = await response.json()
                if response.status != 201:
                    return await InteractionResponse.response_error(
                        interaction,
                        message="add testimoni",
                        emoji=InteractionResponse.data["emoji_cross"],
                        error=resp["message"],
                    )
                await InteractionResponse.response_success(
                    interaction,
                    message="success add testimoni",
                    emoji=InteractionResponse.data["emoji_tick"],
                )


def setup(bot):
    bot.add_cog(Set(bot))
