import discord
from discord import app_commands
from discord.ext import commands

from database import Session, get_user_tracked_list


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="mylist", description="Show your tracked anime list")
    async def mylist(self, interaction: discord.Interaction):
        await interaction.response.defer()

        session = Session()
        tracked = get_user_tracked_list(session, interaction.user.id)
        session.close()


        if not tracked:
            await interaction.followup.send("You're not tracking any anime yet!")
            return

        embed = discord.Embed(
            title="Your Tracked Anime",
            colour=discord.Colour.blue(),
        )
        for anime in tracked:
            embed.add_field(
                name=anime.title,
                value=f"Status: {anime.status}",
                inline=False,
            )
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))

