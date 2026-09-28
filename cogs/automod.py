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
            await message.delete()

            log_channel = self.bot.get_channel(1429740759094919278)
            if log_channel:
                embed = discord.Embed(
                    title="Member Muted",
                    description=f"{message.author.mention} was timed out for posting in <#{1554025555681083453}>",
                    color=discord.Color.orange()
                )
                embed.set_footer(text=f"User ID: {message.author.id}")
                await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AutoMod(bot))