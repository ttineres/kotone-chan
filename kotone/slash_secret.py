#
# slash_secret.py
#


import discord
from discord.ext import commands

from .util_emoji import replace_idol_emoji


class SecretCog(commands.Cog):
    """ A cog for storing secret texts to be revealed later. """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # A set of users currently using anchor
        self.active_users = set()
        # A dict of user-specified secrets
        self.user_secrets = {}
        # A dict of user-specific channels
        self.user_channels = {}

    # Class scope command group
    group = discord.app_commands.Group(name="secret", description="秘密テキスト管理ツール")

    @group.command(name="set", description="秘密テキストを設定")
    @discord.app_commands.rename(content="内容")
    async def set_secret(self, interaction: discord.Interaction, content: str):
        """ A command for storing secret texts. """
        # Check channel is in a guild
        if not interaction.guild:
            await interaction.response.send_message(
                "このチャンネルでこのコマンドを使うことはできません。",
                ephemeral=True
            )
            return
        
        # Check bot is added to guild
        if interaction.guild not in self.bot.guilds:
            await interaction.response.send_message(
                "このサーバーに加入していないため、秘密テキストを設定することができません。",
                ephemeral=True
            )
            return
        
        # Check bot permission to send message in channel
        bot_member = interaction.guild.get_member(self.bot.user.id)
        if not interaction.channel.permissions_for(bot_member).send_messages:
            await interaction.response.send_message(
                "このチャンネルにアクセスできません。チャンネル権限を調整するか、他のチャンネルでこのコマンドを使ってください。",
                ephemeral=True
            )
            return

        # Check user does not have active secrets
        author = interaction.user.name
        if author in self.active_users:
            await interaction.response.send_message(
                "既に保管中の秘密テキストがあります。キャンセルする場合は`/secret cancel`を使ってください。",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            "秘密テキストを預かりました。\n"
            f"内容は「{ replace_idol_emoji(content) }」です。\n"
            "公開する際は`/secret reveal`を使ってください。\n"
            "`一定の期間内に秘密テキストを公開しない場合、コマンドが失効になる可能性があります。`",
            ephemeral=True
        )

        self.active_users.add(author)
        self.user_secrets[author] = content
        self.user_channels[author] = interaction.channel_id

        author_name = interaction.user.mention
        await interaction.channel.send(
            f"{author_name}さんが秘密テキストを設定しました。"
        )
    
    @group.command(name="reveal", description="秘密テキストを公開")
    async def reveal_secret(self, interaction: discord.Interaction):
        author = interaction.user.name
        if author not in self.active_users:
            await interaction.response.send_message("保管中の秘密テキストがありません。", ephemeral=True)
            return
        
        if interaction.channel_id != self.user_channels[author]:
            await interaction.response.send_message(
                "秘密テキストは別のチャンネルで保管されているため、公開できません。\n"
                "キャンセルする場合は`/secret cancel`を使ってください。",
                ephemeral=True
                )
            return
        
        self.active_users.remove(author)
        self.user_channels.pop(author, "")
        author_name = interaction.user.mention
        secret_text = self.user_secrets.pop(author, "")
        await interaction.response.send_message(
            f"{author_name}さんが秘密テキストを公開しました！\n"
            f"内容は「{ replace_idol_emoji(secret_text) }」でした。"
        )

    @group.command(name="cancel", description="秘密テキストをキャンセル")
    async def cancel_secret(self, interaction: discord.Interaction):
        author = interaction.user.name
        if author in self.active_users:
            self.active_users.remove(author)
            self.user_channels.pop(author, "")
            secret_text = self.user_secrets.pop(author, "")
            await interaction.response.send_message(
                f"秘密テキスト「{ replace_idol_emoji(secret_text) }」がキャンセルされました。",
                ephemeral=True
                )
        else:
            await interaction.response.send_message("保管中の秘密テキストがありません。", ephemeral=True)
    
    @group.command(name="help", description="秘密テキストのヘルプを表示")
    async def help_secret(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "こちらは秘密テキストを管理するためのツールです。\n"
            "* `/secret set`：秘密テキストを設定する\n"
            "* `/secret reveal`：秘密テキストを公開する\n"
            "* `/secret cancel`：秘密テキストをキャンセルする\n"
            "注意事項：```"
            "* 個人情報・機密情報を入れないでください。\n"
            "* 秘密テキストの設定されたチャンネル以外では、秘密テキストを公開することはできません。\n"
            "* 同時に複数の秘密テキストを設定することはできません。\n"
            "```",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(SecretCog(bot))
