import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
import asyncio

# Load the .env file
load_dotenv()

# Access the variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = os.getenv("SERVER_ID")



# Intents = what events your bot is allowed to receive
intents = discord.Intents.default()
intents.message_content = True  # needed to read message text for prefix commands
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    guild = bot.get_guild(int(SERVER_ID))
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    print(f"Synced {len(synced)} slash commands to {guild.name}")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")



#Error handler have to update later
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument type — check your input.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: `{error.param.name}`")
    elif isinstance(error, commands.CommandNotFound):
        pass  # ignore silently, so typos don't spam errors
    else:
        await ctx.send("An unexpected error occurred.")
        print(error)

#INFO



async def main():
    async with bot:
        await load_cogs()
        await bot.start(BOT_TOKEN)


asyncio.run(main())