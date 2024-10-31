#
# slash/anchor.py
#


import discord
from discord.ext import commands


class Anchor(commands.Cog):
    """ A cog for anchor activities (安価スレ). """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # A set of users currently using anchor
        self.active_users = set()
        # A dict of user-specified prompts
        self.user_prompts = {}

    # Class scope command group
    group = discord.app_commands.Group(name="anchor", description="全自動安価スレ")

    @group.command(name="start", description="自動安価を開始する")
    @discord.app_commands.rename(content="内容", num_msg="リプ数")
    async def start_anchor(self, interaction: discord.Interaction, content: str, num_msg: int):
        """ A command for setting up automated anchor. """
        # Check channel is in a guild
        if not interaction.guild:
            await interaction.response.send_message(
                "このチャンネルでこのコマンドを使うことはできません。",
                ephemeral=True
            )
            return
        
        # Check bot is added to guild
        bot_member = interaction.guild.get_member(self.bot.user.id)
        if not bot_member:
            await interaction.response.send_message(
                "このサーバーに加入していないので、安価スレを作成することはできません。",
                ephemeral=True
            )
            return
        
        # Check bot permission to send message in channel
        if not interaction.channel.permissions_for(bot_member).send_messages:
            await interaction.response.send_message(
                "このチャンネルにアクセスできません。チャンネル権限を調整するか、他のチャンネルでこのコマンドを使ってください。",
                ephemeral=True
            )
            return

        # Check user does not have active anchor
        author = interaction.user.name
        if author in self.active_users:
            await interaction.response.send_message(
                "既に進行中の安価があります。キャンセルする場合は`/anchor cancel`を使ってください。",
                ephemeral=True
            )
            return
        
        # Check correct argument passed
        if num_msg <= 0:
            await interaction.response.send_message("リプ数を1以上に設定してください！", ephemeral=True)
            return
        
        await interaction.response.send_message(
            "安価スレを開始しました！\n"
            f"内容は「{content}」\n"
            f"↓ {num_msg}\n"
            "`一定の期間内に書き込みがない場合、安価スレが失効になる可能性があります。`"
        )

        self.active_users.add(author)
        self.user_prompts[author] = content
        channel = interaction.channel
        author_name = interaction.user.mention

        def check(m: discord.Message):
            # Ignore bot messages
            return (not m.application_id) and (not m.author.bot) and m.channel == channel

        for _ in range(num_msg):
            msg = await self.bot.wait_for("message", check=check)
            if author not in self.active_users:
                return
        
        if author in self.active_users:
            self.active_users.remove(author)
            await channel.send(
                f"{author_name}さん、安価「{self.user_prompts.pop(author, "")}」の結果が出ましたよ！\n"
                f"結果は「{msg.content}」です。"
            )
    
    @group.command(name="cancel", description="自動安価をキャンセルする")
    async def cancel_anchor(self, interaction: discord.Interaction):
        author = interaction.user.name
        if author in self.active_users:
            self.active_users.remove(author)
            await interaction.response.send_message(f"安価「{self.user_prompts.pop(author, "")}」がキャンセルされました。")
        else:
            await interaction.response.send_message("進行中の安価はありません。")
    
    @group.command(name="help", description="安価コマンドのヘルプを表示する")
    async def help_anchor(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "こちらは全自動安価スレを作成するためのツールです。\n"
            "* `/anchor start`：安価を開始する\n"
            "* `/anchor cancel`：安価をキャンセルする\n"
            "注意事項：```"
            "安価コマンドに指定される書き込みは同チャンネルから選出されます。\n"
            "安価スレと関係のない書き込みも安価のカウントに含まれます。\n"
            "同時に複数の安価スレを作成することはできません。\n"
            "```",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Anchor(bot))
