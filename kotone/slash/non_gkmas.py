#
# slash/non_gkmas.py
#


import discord
from discord.ext import commands

from utils.emoji import get_emoji, KOTONE_EMOJI
from utils.voiceline import get_greeting


class NonGKMas(commands.Cog):
    """ A cog for commands unrelated to playing Gakumas. """
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="kotone-help",
        description="ことねちゃんのコマンドを解説する"
    )
    async def kotone_help(self, interaction: discord.Interaction):
        """ Provides helpful information on using Kotone-chan commands. """
        await interaction.response.send_message(
            f"ことねちゃんのコマンドを解説しまーす{ get_emoji() }\n"
            "* `/kotone-help`：ことねちゃんのコマンドを教えます。\n"
            "* `/hatsuboshi`: 初星学園の公式チャンネルから、楽曲や動画一覧が見れます！\n"
            "* `/calculate`：評価値の計算機です！　試験前のパラメータを入力してくださいね。試験後で計算したいなら`/c`を使ってね。\n"
            "* `/kotone-hello`：ことねちゃんが挨拶しますよ！\n"
            "* `!kotone`：とっておきのことねちゃんスタンプを見せちゃいます♪",
            ephemeral=True
        )
    
    @discord.app_commands.command(
        name="kotone-hello",
        description="ことねちゃんに挨拶する"
    )
    async def kotone_hello(self, interaction: discord.Interaction):
        """ Greets the user. """
        await interaction.response.send_message(
            f"{ get_greeting(interaction.user.mention) }"
            f"{ get_emoji(KOTONE_EMOJI) }"
        )

async def setup(bot):
    await bot.add_cog(NonGKMas(bot))
