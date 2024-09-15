#
# commands/gkmas.py
#


import discord
from discord import app_commands
import math
import random

from utils.emoji import KOTONE


A_PLUS = 11500
S = 13000
S_PLUS = 14500

def get_kotone():
    return random.choice(KOTONE)

def param_to_score(param, rank):
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


async def setup(bot):
    @bot.tree.command(
        name="calculate",
        description="「試験前」のパラメータに応じて、A+やSランクに必要な試験スコアを算出する。使用例：/calculate 1000 1000 1000"
    )
    async def calculate(
        interaction: discord.Integration,
        vocal: int,
        dance: int,
        visual: int,
        cap: int = 1500,
    ):
        """ Calculates score required for ranks.
            Parameters are BEFORE exam.
        """
        new_vocal = min(vocal+30, cap)
        new_dance = min(dance+30, cap)
        new_visual = min(visual+30, cap)
        new_sum = new_vocal+new_dance+new_visual
        await interaction.response.send_message(
            f"Parameter sum before exam: `{vocal+dance+visual}`. {get_kotone()}\n"
            f"Parameter sum after exam: `{new_sum}`.\n"
            f"* S+: `{param_to_score(new_sum, S_PLUS)}`\n"
            f"* S : `{param_to_score(new_sum, S)}`\n"
            f"* A+: `{param_to_score(new_sum, A_PLUS)}`\n",
            ephemeral=True
        )
    
    @bot.tree.command(
        name="c",
        description="「試験後」のパラメータに応じて、A+やSランクに必要な試験スコアを算出する。使用例：/c 1000 1000 1000"
    )
    async def calculate(
        interaction: discord.Integration,
        vocal: int,
        dance: int,
        visual: int,
    ):
        """ Calculates score required for ranks.
            Parameters are AFTER exam.
        """
        param_sum = vocal+dance+visual
        await interaction.response.send_message(
            f"Parameter sum after exam: `{param_sum}`. {get_kotone()}\n"
            f"* S+: `{param_to_score(param_sum, S_PLUS)}`\n"
            f"* S : `{param_to_score(param_sum, S)}`\n"
            f"* A+: `{param_to_score(param_sum, A_PLUS)}`\n",
            ephemeral=True
        )
