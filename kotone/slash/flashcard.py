#
# slash/flashcard.py
#


import random
import os
import discord
from discord.ext import commands

from utils.binary_enum import Ephemeral


P_DRINK_FLASHCARD = {
    "初星水"               : "* パラメータ+10",
    "烏龍茶"               : "* __**元気**__+7",
    "ビタミンドリンク"      : "* __**好調**__3ターン",
    "アイスコーヒー"        : "* __**集中**__+3",
    "ルイボスティー"        : "* __**好印象**__+3",
    "ホットコーヒー"        : "* __**やる気**__+3",
    "ミックススムージー"    : "* 手札をすべて入れ替える\n* __**体力回復**__2",
    "リカバリドリンク"      : "* __**体力回復**__6",
    "フレッシュビネガー"    : "* 手札をすべて__**レッスン中強化**__\n* __**体力回復**__3",
    "ブーストエキス"        : "* __**パラメータ上昇量増加**__30%（3ターン）\n* __**消費体力減少3ターン**__\n* __**体力消費**__2",
    "スタミナ爆発ドリンク"  : "* __**絶好調**__1ターン\n* __**元気**__+9",
    "おしゃれハーブティー"  : "* __**好印象**__の100%分パラメータ上昇\n* __**元気**__+3",
    "初星ホエイプロテイン"  : "* __**スキルカード使用数追加**__+1",
    "初星スペシャル青汁"    : "* ランダムな強化済みスキルカード（SSR）を、手札に__**生成**__",
    "厳選初星マキアート"    : "* 以降、ターン終了時、__**集中**__+1",
    "初星ブーストエナジー"  : "* __**絶好調**__2ターン\n* 手札をすべて__**レッスン中強化**__",
    "厳選初星ティー"        : "* 以降、ターン終了時、__**好印象**__+1",
    "厳選初星ブレンド"      : "* 以降、ターン終了時、__**やる気**__+1",
    "特製ハツボシエキス"    : "* 次に使用する__**アクティブスキルカード**__の効果をもう1回発動（1回・1ターン）\n* __**体力消費**__2\n* __**消費体力増加**__1ターン",
}

# Frequenty used P-items
P_ITEM_FLASHCARD_FREQ = {

}

# All P-items
P_ITEM_FLASHCARD = {
    **P_ITEM_FLASHCARD_FREQ,

    # R Sense
    "ばくおんライオン([学園生活]花海咲季)"      : "* ターン開始時、__**好調**__状態の場合、パラメータ+6\n* (レッスン内1回)",
    "ばくおんライオン+([学園生活]花海咲季)"     : "* ターン開始時、__**好調**__状態の場合、パラメータ+11\n* (レッスン内1回)",
    "必携ステンレスボトル([学園生活]月村手毬)"  : "* ターン開始時、__**集中**__が3以上の場合、__**集中**__+4\n* (レッスン内1回)",
    "必携ステンレスボトル+([学園生活]月村手毬)" : "* ターン開始時、__**集中**__が3以上の場合、__**集中**__+6\n* (レッスン内1回)",
    "紳士風ハンカチーフ([学園生活]有村麻央)"    : "* ターン開始時、__**好調**__状態の場合、__**集中**__+1\n* (レッスン内2回)",
    "紳士風ハンカチーフ+([学園生活]有村麻央)"   : "* ターン開始時、__**好調**__状態の場合、__**集中**__+2\n* (レッスン内2回)",
    "いつものメイクポーチ([学園生活]姫崎莉波)"  : "* __**アクティブカード**__使用時、体力が50%以上の場合、__**集中**__+2\n * (レッスン内1回)",
    "いつものメイクポーチ+([学園生活]姫崎莉波)" : "* __**アクティブカード**__使用時、体力が50%以上の場合、__**集中**__+3\n * (レッスン内1回)",
    "ピンクのお揃いブレス([学園生活]紫雲清夏)"  : "* ターン開始時、__**集中**+1\n* (レッスン内2回)",
    "ピンクのお揃いブレス+([学園生活]紫雲清夏)" : "* ターン開始時、__**集中**+1\n* (レッスン内3回)",
    "初声の証・ことね"      : "* __**初めてのご褒美**__使用時、__**好調**__2ターン\n* (レッスン内1回)",
    "初声の証・ことね+"     : "* __**初めてのご褒美**__使用時、__**好調**__2ターン\n* __**固定元気**__+5\n* (レッスン内1回)",
    "初心の証・リーリヤ"    : "* ターン終了時、__**好調**__が6ターン以上の場合、__**好調**__2ターン\n* __**体力消費**__1\n* (レッスン内2回)",
    "初心の証・リーリヤ+"   : "* ターン終了時、__**好調**__が6ターン以上の場合、__**好調**__2ターン\n* (レッスン内2回)",
    "初心の証・千奈"        : "* ターン開始時、最終ターンの場合、パラメータ+2（レッスン中に使用したスキルカード1枚ごとに、パラメータ上昇量+1）\n* __**体力消費**__1\n* (レッスン内1回)",
    "初心の証・千奈+"       : "* ターン開始時、最終ターンの場合、パラメータ+6（レッスン中に使用したスキルカード1枚ごとに、パラメータ上昇量+1）\n* __**体力消費**__1\n* (レッスン内1回)",
    "初恋の証・広"          : "* ターン開始時、体力が50%以下の場合、__**集中**__+2\n* __**消費体力削減**__1\n* ランダムな手札1枚を__**レッスン中強化**__\n* (レッスン内1回)",
    "初恋の証・広+"         : "* ターン開始時、体力が50%以下の場合、__**集中**__+4\n* __**消費体力削減**__2\n* ランダムな手札1枚を__**レッスン中強化**__\n* (レッスン内1回)",

    # R Logic
    "ちびども手作りメダル([学園生活]藤田ことね)"    : "* ターン終了時、__**好印象**__が6以上の場合、__**好印象**__+2\n* (レッスン内2回)",
    "ちびども手作りメダル+([学園生活]藤田ことね)"   : "* ターン終了時、__**好印象**__が6以上の場合、__**好印象**__+2\n* (レッスン内3回)",
    "超絶あんみんマスク([学園生活]篠澤広)"          : "* ターン開始時、最終ターンの場合、__**元気**__の50%分パラメータ上昇\n* __**体力消費**__1",
    "超絶あんみんマスク+([学園生活]篠澤広)"         : "* ターン開始時、最終ターンの場合、__**元気**__の70%分パラメータ上昇\n* __**体力消費**__1",
    "緑のお揃いブレス([学園生活]葛城リーリヤ)"      : "* __**好印象**__が増加後、__**好印象**__+3\n* (レッスン内1回)",
    "緑のお揃いブレス+([学園生活]葛城リーリヤ)"     : "* __**好印象**__が増加後、__**好印象**__+5\n* (レッスン内1回)",
    "願いを叶えるお守り([学園生活]倉本千奈)"        : "* __**やる気**__が増加後、__**やる気**__+2\n* (レッスン内1回)",
    "願いを叶えるお守り+([学園生活]倉本千奈)"       : "* __**やる気**__が増加後、__**やる気**__+3\n* (レッスン内1回)",
    "テクノドッグ([学園生活]花海佑芽)"              : "* スキルカード使用後、__**やる気**__が3以上の場合、__**やる気**__+2\n* (レッスン内1回)",
    "テクノドッグ+([学園生活]花海佑芽)"             : "* スキルカード使用後、__**やる気**__が3以上の場合、__**やる気**__+3\n* (レッスン内1回)",
    "初声の証・咲季" : "* レッスン中に体力が減少した時、__**好印象**__+2\n* (レッスン内2回)",
    "初声の証・咲季+": "* レッスン中に体力が減少した時、__**好印象**__+2\n* (レッスン内3回)",
    "初声の証・手毬" : "* ターン終了時、__**好印象**__が6以上の場合、__**好印象**__の100%分パラメータ上昇\n* (レッスン内2回)",
    "初声の証・手毬+": "* ターン終了時、__**好印象**__が6以上の場合、__**好印象**__の100%分パラメータ上昇\n* (レッスン内3回)",
    "初心の証・莉波" : "* スキルカードを3回使用するごとに、__**やる気**__+2\n* (レッスン内2回)",
    "初心の証・莉波+": "* スキルカードを3回使用するごとに、__**やる気**__+3\n* (レッスン内2回)",
    "初恋の証・麻央" : "* ターン開始時、__**やる気**__が3以上の場合、__**好印象**__+3\n* __**やる気減少**__1\n* (レッスン内1回)",
    "初恋の証・麻央+": "* ターン開始時、__**やる気**__が3以上の場合、__**好印象**__+3\n* __**やる気減少**__1\n* (レッスン内2回)",
    "初恋の証・清夏" : "* スキルカード使用後、__**やる気**__が8以上の場合、__**やる気**__の150%分パラメータ上昇\n* __**体力消費**__1\n* (レッスン内2回)",
    "初恋の証・清夏+": "* スキルカード使用後、__**やる気**__が8以上の場合、__**やる気**__の210%分パラメータ上昇\n* __**体力消費**__1\n* (レッスン内2回)",

    # SR Sense
    # SR Logic
    # SR Support - parts are included in P_ITEM_FLASHCARD_FREQ
    # SR New
    # SSR - parts are included in P_ITEM_FLASHCARD_FREQ
}

SKILLCARD_SENSE_FLASHCARD = {

}

SKILLCARD_LOGIC_FLASHCARD = {

}


def quiz_from(flashcard_dict, ques_using_key):
    """ Generates a quiz text from a random pair in the dict.
        If ques_using_key, uses key as question and value as answer.
        Otherwise, uses value as question and key as answer.
        Returns a pair (question_only_text, full_text).
    """
    match flashcard_dict:
        case d if d == P_DRINK_FLASHCARD:
            header_q_only = "Pドリンクの単語帳から出題します！\n"
            header_full = "正解はこちら！\n"

    key = random.choice(list(flashcard_dict.keys()))
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


class Flashcard(commands.Cog):
    """ A cog for flashcard activities. """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Class scope command group
    group = discord.app_commands.Group(name="flashcard", description="学マス単語帳")

    @group.command(name="drink", description="Pドリンク単語帳から出題")
    @discord.app_commands.rename(ephemeral="表示設定")
    async def p_drink_flashcard(self, interaction: discord.Interaction, ephemeral: Ephemeral = Ephemeral.T):
        """ Interactive quiz from P-drink flashcards. """
        new_ques_text, new_full_text = quiz_from(P_DRINK_FLASHCARD, True)
        await interaction.response.send_message(
            content=new_ques_text,
            view=QuesPreView(P_DRINK_FLASHCARD, True, new_full_text),
            ephemeral=bool(ephemeral.value),
            delete_after=43200
        )
    
    @group.command(name="help", description="学マス単語帳のヘルプを表示")
    async def help_flashcard(self, interaction: discord.Interaction):
        """ Command for help with `/flashcard`. """
        timestamp_modified = int(os.path.getmtime(__file__))

        await interaction.response.send_message(
            "こちらは学マスの単語帳ツールです。学マス用語の暗記にぜひ活用してください！\n"
            "* `/flashcard drink`：Pドリンクの単語帳から出題\n"
            #"* `/flashcard item`：よく使われるPアイテムの単語帳から出題\n"
            #"* `/flashcard item-all`：すべてのPアイテムの単語帳から出題\n"
            #"* `/flashcard sense-card`：よく使われるセンスプランのスキルカードの単語帳から出題\n"
            #"* `/flashcard logic-card`：よく使われるロジックプランのスキルカードの単語帳から出題\n"
            #"* `/flashcard card`：すべてのスキルカードの単語帳から出題\n"
            f"更新日：<t:{timestamp_modified}:D>",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Flashcard(bot))
