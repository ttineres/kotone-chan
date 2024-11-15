#
# test_exclamation_misc.py
#


import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_hello_command(bot, mock_reply, mock_ctx):
    with (
        patch("kotone.util_voiceline.get_greeting") as mock_greeting,
        patch("kotone.util_emoji.get_emoji") as mock_emoji
    ):
        mock_greeting.return_value = "あの……忙しそうですけど、ちゃんと休んでます？"
        mock_emoji.return_value = "<:kotone1:1285561438651285545>"

        await bot.load_extension("kotone.exclamation_misc")

        command = bot.get_command("hello")
        await command(mock_ctx)
        mock_reply.assert_called_once_with(mock_greeting.return_value + mock_emoji.return_value)
    
        await bot.unload_extension("kotone.exclamation_misc")
