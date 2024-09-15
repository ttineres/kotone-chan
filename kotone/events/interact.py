#
# events/interact.py
#


from discord.ext import commands

from kotone.utils.emoji import KOTONE_2
from kotone.cogs.misc import greeting


class Interact(commands.Cog):
    """ A class for user interactions. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"{member.mention}さん、{greeting()}！")
            await channel.send(KOTONE_2)


async def setup(bot):
    await bot.add_cog(Interact(bot))
