import discord
from discord import app_commands
from discord.ext import commands
from ani_search import AnimeSearch
AS = AnimeSearch()

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="search", description="Search anime")
    @app_commands.describe(anime="Name of the anime to search for")
    async def search(self, interaction: discord.Interaction, anime: str):
        await interaction.response.defer()
        ani_data = AS.search_anime(anime)
        embed = discord.Embed(
            title=f"Search results for {anime}",
            color=discord.Color.green()
        )
        for i, item in enumerate(ani_data, start=1):
            embed.add_field(
                name=f"{i}. {item['title']}",
                value=(
                    f"Episodes: {item.get('episodes', 'Unknown')}\n"
                    f"ID: {item.get('id')}"
                ),
                inline=False
            )

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Anime(bot))
