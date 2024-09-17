#
# cogs/misc.py
#


from discord.ext import commands
import random

from utils.emoji import get_emoji, KOTONE_EMOJI
from utils.voiceline import get_greeting, SPECIAL_KEYWORDS_GREETING, get_greeting_special


class Miscellaneous(commands.Cog):
    """ A cog for miscellaneous commands. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hello")
    async def hello(self, ctx, *, arg=None):
        """ Greets the user.
            Certain keywords in arg trigger special interaction.
        """
        if arg:
            keywords = SPECIAL_KEYWORDS_GREETING.copy()
            random.shuffle(keywords)
            for keyword in keywords:
                if keyword in arg:
                    await ctx.reply(get_greeting_special(ctx.author.mention, keyword))
                    return

        await ctx.reply(
            f"{ get_greeting(ctx.author.mention) }"
            f"{ get_emoji(KOTONE_EMOJI) }"
        )
    
    
    @commands.command(name="kotone")
    async def kotone(self, ctx):
        """ Sends Kotone emoji. """
        await ctx.send(get_emoji())
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
