#
# slash_gkmas.py
#


import discord
from discord.ext import commands
import math
import random
from typing import Literal

from .util.emoji import get_emoji, P_ITEM_EMOJI
from .util.binary_enum import EphemeralEnum


A_PLUS = 11500
S = 13000
S_PLUS = 14500
SS = 16000
SS_PLUS = 18000

def eval_to_rank(eval_: int) -> str:
    """ Converts evaluation score to rank. """
    if eval_ < A_PLUS:
        return "A"
    if eval_ < S:
        return "A+"
    if eval_ < S_PLUS:
        return "S"
    if eval_ < SS:
        return "S+"
    if eval_ < SS_PLUS:
        return "SS"
    return "SS+"

def param_to_score(param: int, rank: int) -> int:
    """ Returns the scores needed for the specified rank. """
    param_total = int(param * 2.3) + 1700
    diff = rank - param_total
    if diff <= 1500:
        return math.ceil(diff / 0.3)
    if diff <= 2250:
        return 5000 + math.ceil((diff-1500) / 0.15)
    if diff <= 3050:
        return 10000 + math.ceil((diff-2250) / 0.08)
    if diff <= 3450:
        return 20000 + math.ceil((diff-3050) / 0.04)
    if diff <= 3650:
        return 30000 + math.ceil((diff-3450) / 0.02)
    return 40000 + math.ceil((diff-3650) / 0.01)

def nia_estimate_eval(param: int, votes: int, score: int) -> int:
    """ Returns the estimated evaluation given pre-audition
        `param` and `votes`, and the `score` of the final audition.
    """
    score = max(score, 200000)
    return nia_param_to_eval(param + score * 0.003, votes + score / 6)

def nia_param_to_eval(param: int | float, votes: int | float) -> int:
    """ Returns the evaluation score in 'NIA' game mode.

        Calculation is based on parameter sum and votes
        at the end of the game.

        Result is parameter * 2.3 + fan_eval, where

        fan_eval = 1200 + votes * 0.065 if vote-rating is S  (60000 - 80000)
                 = 1600 + votes * 0.06  if vote-rating is S+ (80000 - 100000)
                 = 2100 + votes * 0.055 if vote-rating is SS (100000-)
    """
    eval_total = int(param * 2.3)
    if votes < 80000:
        return eval_total + 1200 + int(votes * 0.065)
    if votes < 100000:
        return eval_total + 1600 + int(votes * 0.06)
    return eval_total + 2100 + int(votes * 0.055)


class GakumasCog(commands.Cog):
    """ A cog for commands related to playing Gakumas. """

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.app_commands.command(
        name="calculate",
        description="定期公演『初』において、A+やSランクに必要な試験スコアを「試験前」のパラメータに応じて算出する"
    )
    @discord.app_commands.rename(cap="パラメータ上限", ephemeral="表示設定")
    async def calculate(
        self,
        interaction: discord.Interaction,
        vo: int,
        da: int,
        vi: int,
        cap: Literal[1500, 1800] = 1800,
        ephemeral: EphemeralEnum = EphemeralEnum.T
    ):
        """ Calculates score required for ranks.
            Parameters are BEFORE exam.
        """
        new_vocal = min(vo+30, cap)
        new_dance = min(da+30, cap)
        new_visual = min(vi+30, cap)
        new_sum = new_vocal + new_dance + new_visual

        # Retrieve unique emojis
        p_item_emoji = P_ITEM_EMOJI.copy()
        emoji_1_key = random.choice([*p_item_emoji.keys()])
        emoji_1 = p_item_emoji.pop(emoji_1_key)
        emoji_2 = get_emoji(p_item_emoji)

        await interaction.response.send_message(
            "```このコマンドは定期公演『初』にのみ対応しています。『NIA』の計算は /nia をお使いください。```"
            f"試験前パラメータ合計：`{ vo + da + vi }`\t{ emoji_1 }\n"
            f"試験後パラメータ合計：`{ new_sum }`\t{ emoji_2 }\n"
            f"* SS: `{ param_to_score(new_sum, SS) }`\n"
            f"* S+: `{ param_to_score(new_sum, S_PLUS) }`\n"
            f"* S : `{ param_to_score(new_sum, S) }`\n"
            f"* A+: `{ param_to_score(new_sum, A_PLUS) }`\n",
            ephemeral=bool(ephemeral.value)
        )


    @discord.app_commands.command(
        name="c",
        description="定期公演『初』において、A+やSランクに必要な試験スコアを「試験後」のパラメータに応じて算出する"
    )
    @discord.app_commands.rename(ephemeral="表示設定")
    async def calculate_post_exam(
        self,
        interaction: discord.Interaction,
        vo: int,
        da: int,
        vi: int,
        ephemeral: EphemeralEnum = EphemeralEnum.T
    ):
        """ Calculates score required for ranks.
            Parameters are AFTER exam.
        """
        param_sum = vo+da+vi
        await interaction.response.send_message(
            "```このコマンドは定期公演『初』にのみ対応しています。『NIA』の計算は /nia をお使いください。```"
            f"試験後パラメータ合計：`{ param_sum }`\t{ get_emoji(P_ITEM_EMOJI) }\n"
            f"* SS: `{ param_to_score(param_sum, SS) }`\n"
            f"* S+: `{ param_to_score(param_sum, S_PLUS) }`\n"
            f"* S : `{ param_to_score(param_sum, S) }`\n"
            f"* A+: `{ param_to_score(param_sum, A_PLUS) }`\n",
            ephemeral=bool(ephemeral.value)
        )


    @discord.app_commands.command(
        name="nia-raw",
        description="『NIA』において、最終パラメータ及び投票数に応じて最終ランクを算出する"
    )
    @discord.app_commands.rename(votes="投票数", ephemeral="表示設定")
    async def calculate_nia(
        self,
        interaction: discord.Interaction,
        vo: int,
        da: int,
        vi: int,
        votes: int,
        ephemeral: EphemeralEnum = EphemeralEnum.T
    ):
        """ Calculates final rank based on
            final parameter sum and votes.
        """
        base_param = vo + da + vi
        final_eval = nia_param_to_eval(base_param, votes)

        # Retrieve unique emojis
        p_item_emoji = P_ITEM_EMOJI.copy()
        emoji_1_key = random.choice([*p_item_emoji.keys()])
        emoji_1 = p_item_emoji.pop(emoji_1_key)
        emoji_2 = get_emoji(p_item_emoji)

        await interaction.response.send_message(
            f"『N.I.A』評価値はこちら！\n"
            f"最終パラメータ合計：`{ base_param }`\t{ emoji_1 }\n"
            f"最終投票数合計：`{ votes }`\t{ emoji_2 }\n"
            f"* 評価値：`{ final_eval }` （{ eval_to_rank(final_eval) }）",
            ephemeral=bool(ephemeral.value)
        )


    @discord.app_commands.command(
        name="nia-estimate",
        description="『NIA』において、最終オーディション前パラメータ、投票数とスコアに応じて推定評価値を算出する"
    )
    @discord.app_commands.rename(votes="投票数", score="スコア", ephemeral="表示設定")
    async def estimate_nia_with_score(
        self,
        interaction: discord.Interaction,
        vo: int,
        da: int,
        vi: int,
        votes: int,
        score: int,
        ephemeral: EphemeralEnum = EphemeralEnum.T
    ):
        """ Calculates final rank based on
            final parameter sum and votes.
        """
        # Retrieve unique emojis
        p_item_emoji = P_ITEM_EMOJI.copy()
        emoji_1_key = random.choice([*p_item_emoji.keys()])
        emoji_1 = p_item_emoji.pop(emoji_1_key)
        emoji_2_key = random.choice([*p_item_emoji.keys()])
        emoji_2 = p_item_emoji.pop(emoji_2_key)
        emoji_3 = get_emoji(p_item_emoji)

        estimate_eval = nia_estimate_eval(vo + da + vi, votes, score)

        await interaction.response.send_message(
            f"『N.I.A』**推定**評価値はこちら！\n"
            f"オーディション前パラメータ合計：`{ vo + da + vi }`\t{ emoji_1 }\n"
            f"オーディション前投票数合計：`{ votes }`\t{ emoji_2 }\n"
            f"最終スコア：`{ score }`\t{ emoji_3 }\n"
            f"* **推定**評価値：`{ estimate_eval }` （{ eval_to_rank(estimate_eval) }）"
            "```"
            "評価値は推定値です。実際の数値と大きく乖離する場合があります。\n"
            "審査基準1位から3位、それぞれのターンに獲得したスコアの割合は考慮されていません。"
            "```",
            ephemeral=bool(ephemeral.value)
        )


    @discord.app_commands.command(
        name="nia",
        description="『NIA』において、S+やSSランクに必要なスコアを「最終オーディション前」の状況に応じて推定評価値を算出する"
    )
    @discord.app_commands.rename(votes="投票数", ephemeral="表示設定")
    async def estimate_nia(
        self,
        interaction: discord.Interaction,
        vo: int,
        da: int,
        vi: int,
        votes: int,
        ephemeral: EphemeralEnum = EphemeralEnum.T
    ):
        """ Estimates the score required for NIA game mode.
            Parameters and votes are BEFORE exam.

            Uses a list of candidate scores to
            approximate the necessary scores for SS and SS+ ranks.
        """
        # Retrieve unique emojis
        p_item_emoji = P_ITEM_EMOJI.copy()
        emoji_1_key = random.choice([*p_item_emoji.keys()])
        emoji_1 = p_item_emoji.pop(emoji_1_key)
        emoji_2 = get_emoji(p_item_emoji)

        base_param = vo + da + vi

        # 20 candidate scores 10000, 20000, ..., 200000
        candidates = range(10000, 200001, 10000)
        candidate_evals = [
            nia_estimate_eval(base_param, votes, score)
            for score
            in candidates
        ]

        rough_score_ss = -1
        rough_score_ss_plus = -1
        for i in range(20):
            if candidate_evals[i] >= SS and rough_score_ss == -1:
                rough_score_ss = (i + 1) * 10000
            if candidate_evals[i] >= SS_PLUS and rough_score_ss_plus == -1:
                rough_score_ss_plus = (i + 1) * 10000

        final_score_ss = -1
        if rough_score_ss != -1:
            for score in range(rough_score_ss - 9000, rough_score_ss + 1, 1000):
                if nia_estimate_eval(base_param, votes, score) >= SS:
                    final_score_ss = score
                    break

        final_score_ss_plus = -1
        if rough_score_ss_plus != -1:
            for score in range(rough_score_ss_plus - 9000, rough_score_ss_plus + 1, 1000):
                if nia_estimate_eval(base_param, votes, score) >= SS_PLUS:
                    rough_score_ss_plus = score
                    break

        message = (
            f"『N.I.A』最終オーディションの**推定**必須スコアはこちら！\n"
            f"オーディション前パラメータ合計：`{ base_param }`\t{ emoji_1 }\n"
            f"オーディション前投票数合計：`{ votes }`\t{ emoji_2 }\n"
        )

        if final_score_ss == -1:
            message += "* SS：無理かも……（`200000`以上？）\n"
        else:
            message += f"* SS：`{ final_score_ss }`\n"

        if final_score_ss_plus == -1:
            message += "* SS+：無理かも……（`200000`以上？）\n"
        else:
            message += f"* SS+：`{ final_score_ss_plus }`\n"

        message += (
            "```"
            "スコアはすべて推定値です。実際の数値と大きく乖離する場合があります。\n"
            "審査基準1位から3位、それぞれのターンに獲得したスコアの割合は考慮されていません。"
            "```"
        )

        await interaction.response.send_message(
            message,
            ephemeral=bool(ephemeral.value)
        )


async def setup(bot):
    await bot.add_cog(GakumasCog(bot))
