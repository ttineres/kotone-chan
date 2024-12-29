#
# event_interact.py
#


import discord
from discord.ext import commands

from .util.emoji import KOTONE_EMOJI
from .util.voiceline import get_greeting_new_member


class InteractCog(commands.Cog):
    """ A cog for user interactions. """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            try:
                await channel.send(get_greeting_new_member(member.mention))
                await channel.send(KOTONE_EMOJI["kotone2"])
            except discord.HTTPException:
                pass


async def setup(bot):
    await bot.add_cog(InteractCog(bot))
