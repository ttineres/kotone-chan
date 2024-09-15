#
# cogs/misc.py
#


from discord.ext import commands

from utils.emoji import get_kotone_emoji
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
            f"{get_kotone_emoji()}"
        )
    
    @commands.command(name="kotone")
    async def kotone(self, ctx):
        """ Sends Kotone emoji. """
        await ctx.send(get_kotone_emoji())
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
