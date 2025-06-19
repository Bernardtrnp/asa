import nextcord
import yaml
from utils import InteractionResponse
from databases import ApiKeyDatabase
import aiohttp


class AddTestimoniModal(nextcord.ui.Modal):
    with open("./configs/config.yaml", "r", encoding="utf8") as f:
        data = yaml.safe_load(f)

    def __init__(self):
        super().__init__("Add Testimoni", timeout=None)

        self.rating = nextcord.ui.TextInput(
            label="Rating",
            min_length=1,
            max_length=50,
            custom_id="rating",
        )
        self.add_item(self.rating)

        self.description = nextcord.ui.TextInput(
            label="Description",
            min_length=2,
            max_length=50,
            custom_id="description",
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await InteractionResponse.response_loading(interaction)
        if not (
            user_data := await ApiKeyDatabase.get(
                "by_discord_id", discord_id=interaction.user.id
            )
        ):
            return await InteractionResponse.response_error(
                interaction,
                message="add vouch",
                emoji=InteractionResponse.data["emoji_cross"],
                error="you don't have api key",
            )

        url = "http://localhost:5000/rakit-app/user/testimoni"
        form = aiohttp.FormData()
        form.add_field("rating", f"{self.rating.value}")
        form.add_field("description", self.description.value)
        form.add_field("discord_id", f"{interaction.user.id}")
        form.add_field("username", f"{interaction.user.name}")
        form.add_field("avatar", f"{interaction.user.avatar}")

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
