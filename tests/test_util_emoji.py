#
# test_util_emoji.py
#


import pytest
from kotone.util_emoji import *


mock_kotone_emoji = {
    "kotone1": "<:kotone1:1285561438651285545>"
}

mock_p_item_emoji = {
    "p_item_chokinbako": "<:p_item_chokinbako:1285442904101490770>"
}

mock_idol_emoji = {
    "saki1": "<:saki1:1285561319361220711>",
}


@pytest.mark.parametrize(("emojis", "possible_outcomes"), (
    ((), (KOTONE_EMOJI | P_ITEM_EMOJI).values()),
    ((mock_kotone_emoji,), [KOTONE_EMOJI["kotone1"]]),
    ((mock_p_item_emoji,), [P_ITEM_EMOJI["p_item_chokinbako"]]),
    ((mock_idol_emoji,), [IDOL_EMOJI["saki1"]]),
    ((mock_idol_emoji, mock_kotone_emoji), [IDOL_EMOJI["saki1"], KOTONE_EMOJI["kotone1"]]),
))
def test_get_emoji(emojis, possible_outcomes):
    assert get_emoji(*emojis) in possible_outcomes


@pytest.mark.parametrize(("emoji", "emoji_name"), (
    (None, None),
    ("<:kotone2:1240868676278812742>", "kotone2"),
    ("<:temari_hlw:1289166801900666931>", "temari_hlw"),
    ("<:yatta:1233992971666329662>", "yatta"),
    (":lilja1:", None),
    ("rinami2", None),
))
def test_emoji_to_name(emoji, emoji_name):
    assert emoji_to_name(emoji) == emoji_name


@pytest.mark.parametrize(("message", "result"), ((
        f"手毬<:temari1:1240868706989641738>",
        f"手毬{ IDOL_EMOJI["temari1"] }"
    ), (
        f"俺<:TheTman:467927310184611841>:今日は<:ques:1247745906816585729>なんだ",
        f"俺<:TheTman:467927310184611841>:今日は{ IDOL_EMOJI["ques"] }なんだ"
    ), (
        f":happy::lucky:<:wakarimasitaka:1247746311252480070> <:character_150KingBoo:1084132570020720701>",
        f":happy::lucky:{ IDOL_EMOJI["wakarimasitaka"]} <:character_150KingBoo:1084132570020720701>"
    ), (
        f"<:ume_hlw:1289166804236894281> <:rinami_hlw:1289166794270965782> <:matane:1222091514126143488>",
        f"{ IDOL_EMOJI["ume_hlw"] } { IDOL_EMOJI["rinami_hlw"] } { IDOL_EMOJI["matane"] }"
    ),
))
def test_replace_idol_emoji(message, result):
    assert replace_idol_emoji(message) == result
