import nextcord
from nextcord import ButtonStyle
import yaml
from modals import AddTestimoniModal


class AddTestimoniUI(nextcord.ui.View):
    with open("./configs/config.yaml", "r", encoding="utf8") as f:
        data_content = yaml.safe_load(f)

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Add Vouch",
        style=ButtonStyle.green,
        custom_id="add_testimoni",
    )
    async def set_growid(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        modal = AddTestimoniModal()
        await interaction.response.send_modal(modal)
