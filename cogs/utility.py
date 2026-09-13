import discord
from discord import app_commands
from discord.ext import commands
from ani_search import AnimeSearch

AS = AnimeSearch()




from database import Session, get_user_tracked_list, get_next_episode, delete_anime_tracking, update_anime


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
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
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

    @app_commands.command(name="update", description="Update an anime")
    async def update(self, interaction: discord.Interaction):
        await interaction.response.defer()
        session = Session()
        tracked_out = get_user_tracked_list(session, interaction.user.id)
        tracked = [t.anime for t in tracked_out]
        session.close()

        if not tracked:
            await interaction.followup.send("You're not tracking any anime yet!")
            return

        await interaction.followup.send(view=AnimeListUpdateView(tracked))








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

class AnimeListUpdateButton(discord.ui.Button):
    def __init__(self, title, anilist_id,status,row):
        super().__init__(label=title,style=discord.ButtonStyle.blurple,row=row)
        self.anilist_id = anilist_id
        self.title = title
        self.status = status

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        session = Session()
        ani_schedule = AS.get_schedule(self.anilist_id)
        schedule = ani_schedule['Media']['airingSchedule']['nodes']
        update_anime(session,self.anilist_id,self.title,self.status,schedule)

        embed = discord.Embed(
            title=f"Schedule for {ani_schedule['Media']['title']['english']}",
            description=f"Next Episode: **{ani_schedule['Media']['nextAiringEpisode']['episode']}**\n"
                        f"Airing At: **<t:{ani_schedule['Media']['nextAiringEpisode']['airingAt']}:F>**",
            color=discord.Color.red()
        )

        for item in schedule:
            embed.add_field(
                name=f"Episode: {item['episode']} - <t:{item['airingAt']}:F>\n",
                value="\n",
                inline=False
            )
        print("sending update message")
        await interaction.edit_original_response(embed=embed, view=None)
        await interaction.followup.send(content=f"{self.title} has been updated.")






class AnimeListUpdateView(discord.ui.View):
    def __init__(self,tracked):
        super().__init__()
        for index , anime in enumerate(tracked):

            self.add_item(
                AnimeListUpdateButton(
                    title=f"{anime.title}",
                    anilist_id=anime.anilist_id,
                    status=anime.status,
                    row=index,
                )
            )
