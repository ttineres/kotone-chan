#
# bot.py
#


import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv

from keep_alive import keep_alive


# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    encoding="utf-8",
    handlers=[logging.StreamHandler()],
)

# Retrieve token from environment variable
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TEST_GUILD = os.getenv("TEST_GUILD")
DEBUGGING = os.getenv("DEBUGGING")

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

# Load commands once bot is ready
@bot.event
async def on_ready():
    logging.info(f"[KOTONE] Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="世界一可愛い私"))

    ignored_files = ["__init__.py"]
    
    # Add exclamation commands
    for f in os.listdir("kotone/exclamation"):
        if f.endswith(".py") and f not in ignored_files:
            logging.info(f"[KOTONE] Adding kotone/exclamation/{f}")
            await bot.load_extension(f"exclamation.{f[:-3]}")

    # Add slash commands
    for f in os.listdir("kotone/slash"):
        if f.endswith(".py") and f not in ignored_files:
            logging.info(f"[KOTONE] Adding kotone/slash/{f}")
            await bot.load_extension(f"slash.{f[:-3]}")
    
    # Add events
    for f in os.listdir("kotone/events"):
        if f.endswith(".py") and f not in ignored_files:
            logging.info(f"[KOTONE] Adding kotone/events/{f}")
            await bot.load_extension(f"events.{f[:-3]}")
    
    if DEBUGGING == "TRUE":
        # immediately synchronize commands to a personal guild for debugging
        guild = discord.Object(id=TEST_GUILD)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        logging.info(f"[KOTONE] DEBUGGING: Updated commands to personal guild successfully.")
    else:
        await bot.tree.sync()
    
    logging.info("[KOTONE] Updated all commands successfully.")

def main():
    keep_alive()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
