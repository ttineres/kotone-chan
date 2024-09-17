#
# non_gkmas.py
#


import discord

from utils.emoji import get_emoji, KOTONE_EMOJI
from utils.voiceline import get_greeting


async def setup(bot):
    @bot.tree.command(
        name="kotone-help",
        description="ことねちゃんのコマンドを解説する"
    )
    async def kotone_help(interaction: discord.Interaction):
        """ Provides helpful information on using Kotone-chan commands.
        """
        await interaction.response.send_message(
            f"ことねちゃんのコマンドを解説しまーす{ get_emoji() }\n"
            "* `/kotone-help`：ことねちゃんのコマンドを教えます。\n"
            "* `/calculate`：評価値の計算機です！　試験前のパラメータを入力してくださいね。試験後で計算したいなら`/c`を使ってね。\n"
            "* `/kotone-hello`：ことねちゃんが挨拶しますよ！\n"
            "* `!kotone`：とっておきのことねちゃんスタンプを見せちゃいます♪",
            ephemeral=True
        )
    
    @bot.tree.command(
        name="kotone-hello",
        description="ことねちゃんに挨拶する"
    )
    async def kotone_hello(interaction: discord.Interaction):
        """ Greets the user. """
        await interaction.response.send_message(
            f"{ get_greeting(interaction.user.mention) }"
            f"{ get_emoji(KOTONE_EMOJI) }"
        )
