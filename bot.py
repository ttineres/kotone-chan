#
# bot.py
#


import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


# Retrieve token from environment variable
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for f in os.listdir("./cogs"):
        if f.endswith(".py") and f != "__init__.py":
            await bot.load_extension(f"cogs.{f[:-3]}")
    print("Loaded all cogs successfully.")
    for f in os.listdir("./slash"):
        if f.endswith(".py") and f != "__init__.py":
            await bot.load_extension(f"slash.{f[:-3]}")
    guild = discord.Object(id=1215942055667171388)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print("Updated all commands successfully.")

bot.run(TOKEN)
