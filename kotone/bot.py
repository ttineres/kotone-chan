#
# bot.py
#


import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive


# Retrieve token from environment variable
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="世界一可愛い私"))
    for f in os.listdir("kotone/cogs"):
        if f.endswith(".py") and f != "__init__.py":
            await bot.load_extension(f"cogs.{f[:-3]}")
    print("Loaded all cogs successfully.")
    for f in os.listdir("kotone/slash"):
        if f.endswith(".py") and f != "__init__.py":
            await bot.load_extension(f"slash.{f[:-3]}")
    for f in os.listdir("kotone/events"):
        if f.endswith(".py") and f != "__init__.py":
            await bot.load_extension(f"events.{f[:-3]}")
    # guild is for testing on a personal server
    # guild = discord.Object(id=1215942055667171388)
    # bot.tree.copy_global_to(guild=guild)
    # await bot.tree.sync(guild=guild)
    await bot.tree.sync()
    print("Updated all commands successfully.")

keep_alive()
bot.run(TOKEN)
