#
# slash_flashcard.py
#


import random
import discord
from discord.ext import commands

from .util.binary_enum import EphemeralEnum
from .flashcard.init_flashcard import (
    _FLASHCARD_P_DRINKS,
    _FLASHCARD_P_ITEMS_FREQ,
    _FLASHCARD_P_ITEMS,
    _FLASHCARD_SKILLCARDS_FREQ,
    _FLASHCARD_SKILLCARDS,
)


def quiz_from(flashcard_dict, ques_using_key):
    """ Generates a quiz text from a random pair in the dict.
        If ques_using_key, uses key as question and value as answer.
        Otherwise, uses value as question and key as answer.
        Returns a pair (question_only_text, full_text).
    """
    header_q_only = f"「{flashcard_dict["desc"]}」の単語帳から出題します！\n"
    header_full = "正解はこちら！\n"

    key = random.choice(list( flashcard_dict.keys() - {"desc"} ))
    value = flashcard_dict[key]
    if ques_using_key:
        return (
            header_q_only + f"名称：**{key}**\n効果：？？？",
            header_full + f"名称：**{key}**\n効果：\n{value}"
        )
    else:
        return (
            header_q_only + f"名称：？？？\n効果：\n{value}",
            header_full + f"名称：**{key}**\n効果：\n{value}"
    )


class QuesPostView(discord.ui.View):
    """ View for quiz including both question and answer. """
    def __init__(self, flashcard_dict, ques_using_key):
        """ `flashcard_dict` is a dict of card names and effects.
            `ques_using_key` is a boolean indicating whether
            question uses dict key; see `quiz_from()`.
        """
        super().__init__(timeout=None)
        self.flashcard_dict = flashcard_dict
        self.ques_using_key = ques_using_key

    @discord.ui.button(label="新しく出題", style=discord.ButtonStyle.blurple, row=1)
    async def new_quiz_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_ques_text, new_full_text = quiz_from(self.flashcard_dict, self.ques_using_key)
        await interaction.response.edit_message(content=new_ques_text, view=QuesPreView(self.flashcard_dict, self.ques_using_key, new_full_text))

    @discord.ui.button(label="出題モード変更", style=discord.ButtonStyle.grey, row=1)
    async def opposite_quiz_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_ques_text, new_full_text = quiz_from(self.flashcard_dict, not self.ques_using_key)
        await interaction.response.edit_message(content=new_ques_text, view=QuesPreView(self.flashcard_dict, not self.ques_using_key, new_full_text))

class QuesPreView(QuesPostView):
    """ View for quiz before answer is revealed. """
    def __init__(self, flashcard_dict, ques_using_key, full_text):
        """ `flashcard_dict` is a dict of card names and effects.
            `ques_using_key` is a boolean indicating whether
            question uses dict key; see `quiz_from()`.
            `full_text` is a string of full quiz text.
        """
        super().__init__(flashcard_dict, ques_using_key)
        self.full_text = full_text

    @discord.ui.button(label="答えを見る", style=discord.ButtonStyle.green, row=0)
    async def post_view_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=self.full_text, view=QuesPostView(self.flashcard_dict, self.ques_using_key))


class FlashcardCog(commands.Cog):
    """ A cog for flashcard activities. """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Class scope command group
    group = discord.app_commands.Group(name="flashcard", description="学マス単語帳")

    @group.command(name="drink", description="Pドリンクの単語帳から出題")
    @discord.app_commands.rename(ephemeral="表示設定")
    async def p_drink_flashcard(self, interaction: discord.Interaction, ephemeral: EphemeralEnum = EphemeralEnum.T):
        """ Interactive quiz from P-drink flashcards. """
        new_ques_text, new_full_text = quiz_from(_FLASHCARD_P_DRINKS, True)
        await interaction.response.send_message(
            content=new_ques_text,
            view=QuesPreView(_FLASHCARD_P_DRINKS, True, new_full_text),
            ephemeral=bool(ephemeral.value)
        )

    @group.command(name="item", description="よく使われるPアイテムの単語帳から出題")
    @discord.app_commands.rename(ephemeral="表示設定")
    async def p_item_flashcard(self, interaction: discord.Interaction, ephemeral: EphemeralEnum = EphemeralEnum.T):
        """ Interactive quiz from P-item flashcards. """
        new_ques_text, new_full_text = quiz_from(_FLASHCARD_P_ITEMS_FREQ, True)
        await interaction.response.send_message(
            content=new_ques_text,
            view=QuesPreView(_FLASHCARD_P_ITEMS_FREQ, True, new_full_text),
            ephemeral=bool(ephemeral.value)
        )

    @group.command(name="item-all", description="すべてのPアイテムの単語帳から出題")
    @discord.app_commands.rename(ephemeral="表示設定")
    async def p_item_all_flashcard(self, interaction: discord.Interaction, ephemeral: EphemeralEnum = EphemeralEnum.T):
        """ Interactive quiz from all P-item flashcards. """
        new_ques_text, new_full_text = quiz_from(_FLASHCARD_P_ITEMS, True)
        await interaction.response.send_message(
            content=new_ques_text,
            view=QuesPreView(_FLASHCARD_P_ITEMS, True, new_full_text),
            ephemeral=bool(ephemeral.value)
        )

    @group.command(name="skill", description="よく使われるスキルカードの単語帳から出題")
    @discord.app_commands.rename(ephemeral="表示設定")
    async def skillcard_flashcard(self, interaction: discord.Interaction, ephemeral: EphemeralEnum = EphemeralEnum.T):
        """ Interactive quiz from skillcard flashcards. """
        new_ques_text, new_full_text = quiz_from(_FLASHCARD_SKILLCARDS_FREQ, True)
        await interaction.response.send_message(
            content=new_ques_text,
            view=QuesPreView(_FLASHCARD_SKILLCARDS_FREQ, True, new_full_text),
            ephemeral=bool(ephemeral.value)
        )

    @group.command(name="skill-all", description="すべてのスキルカードの単語帳から出題")
    @discord.app_commands.rename(ephemeral="表示設定")
    async def skillcard_flashcard(self, interaction: discord.Interaction, ephemeral: EphemeralEnum = EphemeralEnum.T):
        """ Interactive quiz from all skillcard flashcards. """
        new_ques_text, new_full_text = quiz_from(_FLASHCARD_SKILLCARDS, True)
        await interaction.response.send_message(
            content=new_ques_text,
            view=QuesPreView(_FLASHCARD_SKILLCARDS, True, new_full_text),
            ephemeral=bool(ephemeral.value)
        )

    @group.command(name="help", description="学マス単語帳のヘルプを表示")
    async def help_flashcard(self, interaction: discord.Interaction):
        """ Command for help with `/flashcard`. """
        await interaction.response.send_message(
            "こちらは学マスP図鑑の単語帳ツールです。学マス用語の暗記にぜひ活用してください！\n"
            "* `/flashcard drink`：「Pドリンク」の単語帳から出題\n"
            "* `/flashcard item`：「よく使われるPアイテム」の単語帳から出題\n"
            "* `/flashcard item-all`：「すべてのPアイテム」の単語帳から出題\n"
            "* `/flashcard skill`：「よく使われるスキルカード」の単語帳から出題\n"
            "* `/flashcard skill-all`：「すべてのスキルカード」の単語帳から出題\n",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(FlashcardCog(bot))
