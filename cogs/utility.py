import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime



from database import Session, get_user_tracked_list, get_next_episode, delete_anime_tracking


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="mylist", description="Show your tracked anime list")
    async def mylist(self, interaction: discord.Interaction):
        await interaction.response.defer()

        session = Session()
        tracked_out = get_user_tracked_list(session, interaction.user.id)

        tracked = [t.anime for t in tracked_out]



        if not tracked:
            await interaction.followup.send("You're not tracking any anime yet!")
            return

        embed = discord.Embed(
            title="Your Tracked Anime",
            colour=discord.Colour.blue(),
        )
        for anime in tracked:
            next_ep = get_next_episode(anime)


            if next_ep:

                when = f"<t:{next_ep.airing_at}:F>"
                next_ep_text = f"Next Episode: {next_ep.episode_number} — {when}"

            else:
                next_ep_text = "No upcoming episodes"


            embed.add_field(
                name=anime.title,
                value=f"Status: {anime.status}\n{next_ep_text}",
                inline=False,
            )
        await interaction.followup.send(embed=embed)
        session.close()


    @app_commands.command(name="untrack", description="Untrack an anime")
    async def untrack(self, interaction: discord.Interaction):
        await interaction.response.defer()
        session = Session()
        tracked_out = get_user_tracked_list(session, interaction.user.id)
        tracked = [t.anime for t in tracked_out]
        session.close()


        if not tracked:
            await interaction.followup.send("You're not tracking any anime yet!")
            return

        await interaction.followup.send(view=AnimeListView(tracked))





async def setup(bot):
    await bot.add_cog(Utility(bot))



class AnimeListButton(discord.ui.Button):
    def __init__(self, title, anime_id,row):
        super().__init__(label=title, style=discord.ButtonStyle.red,row=row)
        self.anime_id = anime_id
        self.title = title

    async def callback(self, interaction: discord.Interaction):
        session = Session()
        delete_anime_tracking(session,interaction.user.id, anime_id=self.anime_id)
        await interaction.response.edit_message(content=f"{self.title} has been removed from tracking.",view=None)

class AnimeListView(discord.ui.View):
    def __init__(self,tracked):
        super().__init__()
        for index , anime in enumerate(tracked):

            self.add_item(
                AnimeListButton(
                    title=f"{anime.title}",
                    anime_id=anime.id,
                    row=index,
                )
            )