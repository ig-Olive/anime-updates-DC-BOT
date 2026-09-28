from discord.ext import commands
from datetime import timedelta
import discord


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1554025555681083453 and not message.author.bot:
            await message.author.timeout(timedelta(minutes=720))
            await message.channel.send(f"The user {message.author.name}/{message.author.id} got muted,")


async def setup(bot):
    await bot.add_cog(AutoMod(bot))