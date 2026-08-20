import discord
from discord import app_commands
from discord.ext import commands
from ani_search import AnimeSearch
from datetime import datetime
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
                    f"Status: {item.get('status', 'Unknown')}\n"
                    
                    f"ID: {item.get('id')}\n"
                    f"Episodes: {item.get('episodes', 'Unknown')}\n"

                ),
                inline=False
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="get_schedule", description="Get schedule")
    @app_commands.describe(id="id of the anime to get schedule")
    async def get_schedule(self, interaction: discord.Interaction, id: int):
        await interaction.response.defer()
        ani_schedule = AS.get_schedule(id)
        embed = discord.Embed(
            title=f"Schedule for {ani_schedule['Media']['title']['english']}",
            description=f"Next Episode: {ani_schedule['Media']['nextAiringEpisode']['episode']}\n"
                        f"Airing At: {datetime.fromtimestamp(ani_schedule['Media']['nextAiringEpisode']['airingAt']).strftime("%B %d, %Y - %I:%M %p")}",
        )
        for item in ani_schedule['Media']['airingSchedule']['nodes']:
            embed.add_field(
                name=f"Episode: {item['episode']}",
                value=(
                    f"Airing At: {datetime.fromtimestamp(item['airingAt']).strftime("%B %d, %Y - %I:%M %p")}"
                ),
                inline=False
            )

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Anime(bot))
