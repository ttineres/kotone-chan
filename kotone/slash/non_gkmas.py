#
# non_gkmas.py
#


import discord
import random

from utils.emoji import KOTONE


def get_kotone():
    return random.choice(KOTONE)

async def setup(bot):
    @bot.tree.command(
        name="kotone-help",
        description="ことねちゃんのコマンドを解説する"
    )
    async def kotone_help(
        interaction: discord.Integration,
    ):
        """ Provides helpful information on using Kotone-chan commands.
        """
        await interaction.response.send_message(
            f"ことねちゃんのコマンドを解説しまーす{get_kotone()}\n"
            "* `/kotone-help`：ことねちゃんのコマンドを教えます。\n"
            "* `/calculate`：評価値の計算機です！　試験前のパラメータを入力してくださいね。試験後で計算したいなら`/c`を使ってね。\n"
            "* `!hello`：ことねちゃんが挨拶しますよ！\n"
            "* `!kotone`：とっておきのことねちゃんスタンプを見せちゃいます♪",
            ephemeral=True
        )
