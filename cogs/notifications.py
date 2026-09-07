from discord.ext import commands, tasks
from database import Session, get_due_notifications

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_notifications.start()

    @tasks.loop(minutes=10)
    async def check_notifications(self):
        session = Session()
        due = get_due_notifications(session)
        session.close()

        for notice in due:
            user = await self.bot.fetch_user(int(notice["discord_id"]))
            await user.send(
                f"📺 **{notice['anime_title']}** — Episode {notice['episode_number']} just aired!"
            )

    @check_notifications.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    @check_notifications.error
    async def check_notifications_error(self, error):
        print(f"notification loop error: {error}")

async def setup(bot):
    await bot.add_cog(Notifications(bot))