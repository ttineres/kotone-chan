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
    
    @discord.app_commands.command(
        name="goldrush",
        description="学園アイドルマスター GOLD RUSH の情報はこちら！"
    )
    @discord.app_commands.rename(ephemeral="表示設定")
    @discord.app_commands.choices(ephemeral=[
        discord.app_commands.Choice(name="自分だけに表示", value=1),
        discord.app_commands.Choice(name="全体表示", value=0)
    ])
    async def goldrush(
        self,
        interaction: discord.Interaction,
        ephemeral: discord.app_commands.Choice[int]=None
    ):
        """ Provides useful links to Gold Rush"""
        ephemeral_flag = True
        if ephemeral:
            ephemeral_flag = bool(ephemeral.value)
        
        await interaction.response.send_message(
            f"おっ待たせー！　学園アイドルマスター GOLD RUSH の情報でーす{ get_emoji(KOTONE_EMOJI) }\n"
            "* [第1話や最新話はこちら！](https://championcross.jp/series/f67370b40ec1a)\n"
            "* [掲載誌の最新情報はこちら！](https://www.akitashoten.co.jp/w-champion)\n"
            "* [公式アカウント（@gkmas_GR）はこちら！](https://x.com/gkmas_GR)",
            ephemeral=ephemeral_flag,
            suppress_embeds=True
        )


async def setup(bot):
    await bot.add_cog(NonGKMas(bot))
