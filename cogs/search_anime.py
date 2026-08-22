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
        if not len(ani_data) == 0:
            await interaction.followup.send(view=AnimeView(result=ani_data))
        else:
            await interaction.followup.send("No anime found. :(")


async def setup(bot):
    await bot.add_cog(Anime(bot))




class AnimeButton(discord.ui.Button):
    def __init__(self, anime_id, title,status, row):
        if status == "RELEASING":
            button_type=discord.ButtonStyle.success
        else:
            button_type=discord.ButtonStyle.secondary
        super().__init__(label=title, style=button_type, row=row)
        self.anime_id = anime_id

    async def callback(self, interaction: discord.Interaction):
        ani_schedule = AS.get_schedule(self.anime_id)
        embed = discord.Embed(
            title=f"Schedule for {ani_schedule['Media']['title']['english']}",
            description=f"Next Episode: **{ani_schedule['Media']['nextAiringEpisode']['episode']}**\n"
                        f"Airing At: **{datetime.fromtimestamp(ani_schedule['Media']['nextAiringEpisode']['airingAt']).strftime('%B %d - %I:%M %p')}**",
            color=discord.Color.red()
        )
        for item in ani_schedule['Media']['airingSchedule']['nodes']:
            embed.add_field(
                name=f"Episode: {item['episode']} - {datetime.fromtimestamp(item['airingAt']).strftime('%B %d')}\n",
                value="\n",
                inline=False
            )
        await interaction.response.edit_message(embed=embed,view=None)


class AnimeView(discord.ui.View):
    def __init__(self, result):
        super().__init__()
        for index ,ani in enumerate(result):
            self.add_item(AnimeButton(ani['id'], ani['title'], status=ani.get('status', 'Unknown'), row=index))

