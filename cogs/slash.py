import discord
from discord import app_commands
from discord.ext import commands

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="ping", description="Replies with Pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="greet", description="Greet someone")
    @app_commands.describe(user="Who to greet")
    async def greet(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f"Hello {user.mention}!")


async def setup(bot):
    await bot.add_cog(Slash(bot))
