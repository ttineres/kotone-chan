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

def nia_estimate_eval(
        param: int,
        votes: int,
        score: int,
        is_pessimistic: bool = True
    ) -> int:
    """ Returns the estimated evaluation given pre-audition
        `param` and `votes`, and the `score` of the final audition.

        `is_pessimistic` determines the heuristic values used in
        the estimation.

        Heuristics are partially based on observations by `@_genki_P`.
    """
    # `ratio_score_to_param` is a heuristic value for
    # estimating the post-audition increment of parameter.
    # Commonly observed values range between `180` and `320`.
    ratio_score_to_param = 320 if is_pessimistic else 180

    # `votes_bottleneck` is a heuristic value for
    # estimating the post-audition increment of votes.
    # If the final score is lower than this value,
    # the votes gained is kept at 16,000.
    votes_bottleneck = 80000 if is_pessimistic else 0

    if score <= 199203:
        new_param = param + score / ratio_score_to_param
        new_votes = votes + (35133 - 16000) * (score - votes_bottleneck) / (199203 - votes_bottleneck) + 16000
        new_votes = max(new_votes, 16000)
        naive_estimation = nia_param_to_eval(new_param, new_votes)

        # Compare estimation with another realistic value
        new_param = param + (400 if is_pessimistic else 500)
        new_votes = votes + (38001 - 35133) * (score - 199203) / (796481 - 199203) + 35133
        bottleneck_estimation = nia_param_to_eval(new_param, new_votes)

        return min(naive_estimation, bottleneck_estimation)

    score = min(score, 796481)
    new_param = param + (400 if is_pessimistic else 500 if score < 400000 else 550)
    new_votes = votes + (38001 - 35133) * (score - 199203) / (796481 - 199203) + 35133
    return nia_param_to_eval(new_param, new_votes)

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
        description="『NIA』において、「FINALE前」パラメータ、投票数とスコアに応じて推定評価値を算出する"
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

        base_param = (
            min(vo, 1850)
            + min(da, 1850)
            + min(vi, 1850)
        )
        estimate_eval_pessimistic = nia_estimate_eval(base_param, votes, score, True)
        estimate_eval_optimistic = nia_estimate_eval(base_param, votes, score, False)

        await interaction.response.send_message(
            f"『N.I.A』**推定**評価値はこちら！\n"
            f"「FINALE」前のパラメータ合計：`{ base_param }`\t{ emoji_1 }\n"
            f"「FINALE」前の投票数：`{ votes }`\t{ emoji_2 }\n"
            f"最終スコア：`{ score }`\t{ emoji_3 }\n"
            f"* **推定**評価値：`{ estimate_eval_pessimistic }` ({ eval_to_rank(estimate_eval_pessimistic) })"
            f" ～`{ estimate_eval_optimistic }` ({ eval_to_rank(estimate_eval_optimistic) })\n"
            "```"
            "推測値と実際の評価値が大きく乖離することがあります。"
            "```",
            ephemeral=bool(ephemeral.value)
        )


    @discord.app_commands.command(
        name="nia",
        description="『NIA』において、S+やSSランクに必要なスコアを「FINALE前」の状況に応じて推定評価値を算出する"
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

        base_param = (
            min(vo, 1850)
            + min(da, 1850)
            + min(vi, 1850)
        )

        # Candidate scores 10000, 20000, ..., 200000, 300000, ..., 700000
        candidates = list(range(10000, 200000, 10000)) + list(range(200000, 700001, 100000))

        # Pessimistic estimation
        score_ss_pessimistic = -1
        score_ss_plus_pessimistic = -1
        for candidate_score in candidates:
            candidate_eval = nia_estimate_eval(base_param, votes, candidate_score, True)
            if score_ss_pessimistic == -1 and candidate_eval >= SS:
                score_ss_pessimistic = candidate_score
            if score_ss_plus_pessimistic == -1 and candidate_eval >= SS_PLUS:
                score_ss_plus_pessimistic = candidate_score
                break

        # Optimistic estimation
        score_ss_optimistic = -1
        score_ss_plus_optimistic = -1
        for candidate_score in candidates:
            candidate_eval = nia_estimate_eval(base_param, votes, candidate_score, False)
            if score_ss_optimistic == -1 and candidate_eval >= SS:
                score_ss_optimistic = candidate_score
            if score_ss_plus_optimistic == -1 and candidate_eval >= SS_PLUS:
                score_ss_plus_optimistic = candidate_score
                break

        message = (
            f"『N.I.A』オーディション「FINALE」の**推定**必須スコアはこちら！\n"
            f"「FINALE」前のパラメータ合計：`{ base_param }`\t{ emoji_1 }\n"
            f"「FINALE」前の投票数：`{ votes }`\t{ emoji_2 }\n"
        )

        if score_ss_optimistic == -1:
            message += "* SS：無理かも……（`700000`以上？）\n"
        else:
            message += f"* SS：`{ score_ss_optimistic }`～"
            if score_ss_pessimistic != -1:
                message += f"`{ score_ss_pessimistic }`"
            else:
                message += "`700000+`？"
            message += "\n"

        if score_ss_plus_optimistic == -1:
            message += "* SS+：無理かも……（`700000`以上？）\n"
        else:
            message += f"* SS+：`{ score_ss_plus_optimistic }`～"
            if score_ss_plus_pessimistic != -1:
                message += f"`{ score_ss_plus_pessimistic }`"
            else:
                message += "`700000+`？"
            message += "\n"

        message += (
            "```"
            "推測値と実際の数値が大きく乖離することがあります。"
            "```"
        )

        await interaction.response.send_message(
            message,
            ephemeral=bool(ephemeral.value)
        )


async def setup(bot):
    await bot.add_cog(GakumasCog(bot))
