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


class GakumasCog(commands.Cog):
    """ A cog for commands related to playing Gakumas. """

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.app_commands.command(
        name="calculate",
        description="「試験前」のパラメータに応じて、A+やSランクに必要な試験スコアを算出する"
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
        description="「試験後」のパラメータに応じて、A+やSランクに必要な試験スコアを算出する"
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
            f"試験後パラメータ合計：`{ param_sum }`\t{ get_emoji(P_ITEM_EMOJI) }\n"
            f"* SS: `{ param_to_score(param_sum, SS) }`\n"
            f"* S+: `{ param_to_score(param_sum, S_PLUS) }`\n"
            f"* S : `{ param_to_score(param_sum, S) }`\n"
            f"* A+: `{ param_to_score(param_sum, A_PLUS) }`\n",
            ephemeral=bool(ephemeral.value)
        )


async def setup(bot):
    await bot.add_cog(GakumasCog(bot))
