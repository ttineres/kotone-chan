#
# events/interact.py
#


import discord
from discord.ext import commands
from utils.emoji import KOTONE2
from cogs.misc import greeting


class Interact(commands.Cog):
    """ A class for user interactions. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="herehere")
        if channel:
            await channel.send(f"{member.mention}さん、{greeting()}！{KOTONE2}")


async def setup(bot):
    await bot.add_cog(Interact(bot))
