#
# slash_non_gkmas.py
#


import discord
from discord.ext import commands

from .util.emoji import get_emoji, KOTONE_EMOJI
from .util.voiceline import get_greeting
from .util.binary_enum import EphemeralEnum


class NonGakumasCog(commands.Cog):
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
            "* `/calculate`：評価値の計算機です！　試験前のパラメータを使います。試験後で計算したいなら`/c`を使ってね。\n"
            "* `/nia`：『N.I.A』用の最終オーディション推測値計算機です。\n"
            "* `/hatsuboshi`: 初星学園の公式チャンネルから、楽曲や動画一覧が見れます！\n"
            "* `/goldrush`: 学園アイドルマスター GOLD RUSH の便利リンクを確認できます！\n"
            "* `/kotone-hello`：ことねちゃんが挨拶しますよ！\n"
            "* その他のコマンドのヘルプは`help`で検索してください。\n"
            "* `!kotone`：とっておきのことねちゃんスタンプを見せちゃいます♪",
            ephemeral=True
        )

    @discord.app_commands.command(
        name="kotone-hello",
        description="ことねちゃんに挨拶する"
    )
    @discord.app_commands.rename(ephemeral="表示設定")
    async def kotone_hello(self, interaction: discord.Interaction, ephemeral: EphemeralEnum = EphemeralEnum.F):
        """ Greets the user. """
        await interaction.response.send_message(
            f"{ get_greeting(interaction.user.mention) }"
            f"{ get_emoji(KOTONE_EMOJI) }",
            ephemeral=bool(ephemeral.value)
        )

    @discord.app_commands.command(
        name="goldrush",
        description="学園アイドルマスター GOLD RUSH の情報はこちら！"
    )
    @discord.app_commands.rename(ephemeral="表示設定")
    async def goldrush(
        self,
        interaction: discord.Interaction,
        ephemeral: EphemeralEnum = EphemeralEnum.T
    ):
        """ Provides useful links to Gold Rush"""
        await interaction.response.send_message(
            f"おっ待たせー！　学園アイドルマスター GOLD RUSH の情報でーす{ get_emoji(KOTONE_EMOJI) }\n"
            "* [無料配信はこちらから！](https://championcross.jp/series/f67370b40ec1a)\n"
            "* [週刊少年チャンピオンの最新情報はこちら！](https://www.akitashoten.co.jp/w-champion)\n"
            "* [公式アカウント（@gkmas_GR）はこちら！](https://x.com/gkmas_GR)",
            ephemeral=bool(ephemeral.value),
            suppress_embeds=True
        )


async def setup(bot):
    await bot.add_cog(NonGakumasCog(bot))
