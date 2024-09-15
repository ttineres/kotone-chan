#
# cogs/misc.py
#


from discord.ext import commands
import random
from datetime import datetime, timezone

from utils.emoji import KOTONE


class Miscellaneous(commands.Cog):
    """ A cog for miscellaneous commands. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hello")
    async def hello(self, ctx):
        """ Greets the user. """
        await ctx.reply(f"{ctx.author.mention}さん、{greeting()}！{random.choice(KOTONE)}")
    
    @commands.command(name="kotone")
    async def kotone(self, ctx):
        """ Sends Kotone emoji. """
        await ctx.send(random.choice(KOTONE))
        await ctx.message.delete()


def greeting():
    now = datetime.now(timezone.utc)
    if 21 <= now.hour or now.hour < 3:
        return "おはようございまーす"
    if 3 <= now.hour < 9:
        return "こんにちは"
    return "こんばんは"


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
