#
# events/interact.py
#


from discord.ext import commands

from utils.emoji import KOTONE_EMOJI
from utils.voiceline import get_greeting_new_member


class Interact(commands.Cog):
    """ A cog for user interactions. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(get_greeting_new_member(member.mention))
            await channel.send(KOTONE_EMOJI["kotone2"])


async def setup(bot):
    await bot.add_cog(Interact(bot))
