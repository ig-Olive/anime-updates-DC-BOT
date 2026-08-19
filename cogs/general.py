from discord.ext import commands
import discord

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def say(self, ctx, *, text):
        await ctx.send(text)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Info",
            description=f"A Bot to get anime updates",
            color=discord.Color.green(),
        )
        embed.add_field(name="Prefix", value="!", inline=True)
        embed.add_field(name="Language", value="Python", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))