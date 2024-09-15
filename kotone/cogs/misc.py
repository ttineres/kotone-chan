#
# cogs/misc.py
#


from discord.ext import commands
import random

from utils.emoji import KOTONE
from utils.voiceline import greeting


class Miscellaneous(commands.Cog):
    """ A cog for miscellaneous commands. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hello")
    async def hello(self, ctx):
        """ Greets the user. """
        await ctx.reply(
            f"{greeting(ctx.author.mention)}"
            f"{random.choice(KOTONE)}"
        )
    
    @commands.command(name="kotone")
    async def kotone(self, ctx):
        """ Sends Kotone emoji. """
        await ctx.send(random.choice(KOTONE))
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
