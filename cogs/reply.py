import discord
from discord import app_commands
from discord.ext import commands

class Reply(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="reply",
        description="Answer that delphinian as the oracle"
    )
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.describe(msg="The message the oracle should send")
    async def reply(self, interaction: discord.Interaction, msg: str):
        try:
            # 1️⃣ Acknowledge the interaction silently
            await interaction.response.defer(ephemeral=True)

            # 2️⃣ Send the message normally in the channel
            await interaction.channel.send(msg)

            # 3️⃣ Delete the deferred "thinking" message so users see nothing
            await interaction.delete_original_response()

        except discord.Forbidden:
            # Only if bot can't send messages
            await interaction.followup.send(
                "❌ I don't have permission to send messages here.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            # Log other send errors
            print(f"Failed to send message: {e}")

# Setup
async def setup(bot: commands.Bot):
    await bot.add_cog(Reply(bot))
