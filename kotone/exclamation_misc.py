#
# exclamation_misc.py
#


import discord
from discord.ext import commands

from .util_emoji import get_emoji, KOTONE_EMOJI, IDOL_EMOJI, emoji_to_name
from .util_voiceline import get_greeting, SPECIAL_KEYWORDS_GREETING, get_greeting_special


class ExclamationMiscCog(commands.Cog):
    """ A cog for miscellaneous commands. """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hello")
    async def hello(self, ctx, *, arg=None):
        """ Greets the user.
            Certain keywords in arg trigger special interaction.
        """
        if arg:
            keywords = SPECIAL_KEYWORDS_GREETING.keys()
            # Note: the order of keywords is arbitrary
            for keyword in keywords:
                if keyword in arg:
                    await ctx.reply(get_greeting_special(ctx.author.mention, keyword))
                    return

        await ctx.reply(
            f"{ get_greeting(ctx.author.mention) }"
            f"{ get_emoji(KOTONE_EMOJI) }"
        )
    
    @commands.command(name="kotone")
    async def kotone(self, ctx, *, arg=None):
        """ Sends Kotone emoji.
            Optionally, sends the secified idol emoji.
        """
        # Converts arg from emoji format to name
        arg = emoji_to_name(arg) or arg

        # Converts name to emoji
        emoji = IDOL_EMOJI.get(arg, get_emoji())
        await ctx.send(emoji)

        # Attempts to delete input prompt
        # Only works if given "Manage message" permission
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass


async def setup(bot):
    await bot.add_cog(ExclamationMiscCog(bot))
