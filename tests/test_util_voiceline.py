#
# test_util_voiceline.py
#


import pytest
from freezegun import freeze_time
from unittest.mock import patch
from datetime import datetime
from kotone.util_voiceline import *


def test_get_greeting():
    with patch("random.random") as mock_random:
        mock_random.return_value = 0.05
        assert get_greeting("TestName")
        
        mock_random.return_value = 0.15
        assert get_greeting("TestName")

        mock_random.return_value = 0.25
        assert get_greeting("TestName")


@pytest.mark.parametrize(("name", "hour", "possible_results"), (
    ("TestName",  9, ["おっはようございまーす、TestNameさん！", "今日も一日頑張りましょう！"]),
    ("TestName", 12, ["どーも！　TestNameさんもお昼です？", "お弁当で元気チャージしてぇ、午後も頑張りまーす！"]),
    ("TestName", 15, ["さてさて、こっからが本番ですよね！", "可愛いことねちゃんとの時間が始まりますよぉ～"]),
    ("TestName", 18, ["お疲れさまでーす！", "今日も後ちょっと、頑張りましょう！"]),
))
def test_get_aisatu(name, hour, possible_results):
    with freeze_time(datetime(2024, 5, 16, hour, tzinfo=JAPAN_TIMEZONE)):
        assert get_aisatu(name) in possible_results


@pytest.mark.parametrize(("name", "month", "possible_results"), (
    ("TestName",  3, ["来ました……春限定メニューという名の、繁忙期がぁ～！", "TestNameさん、お花見いきましょうよ～", "もう外でレッスンしても、寒くなさそうですね！"]),
    ("TestName",  6, ["TestNameさん、もっと冷房強くなんないんですか～？", "真夏の着ぐるみバイト……さすがに……", "最近、チビ共が海行きたい～って、うるさいんですよ。"]),
    ("TestName",  9, ["フルーツ狩りって、いくつ取れたらお得なんですかね……", "働きやすい気温になってきましたね！", "TestNameさん！　お仕事の秋が来ましたよ！"]),
    ("TestName", 12, ["フルーツ狩りって、いくつ取れたらお得なんですかね……", "働きやすい気温になってきましたね！", "TestNameさん！　お仕事の秋が来ましたよ！"]),
))
def test_get_season_aisatu(name, month, possible_results):
    with freeze_time(datetime(2024, month, 1, tzinfo=JAPAN_TIMEZONE)):
        assert get_season_aisatu(name) in possible_results


@pytest.mark.parametrize(("name", "keyword", "is_special"), (
    ("TestName", "奇遇ね", True),
    ("TestName", None, False),
    ("TestName", "ママうるさい", False),
))
def test_get_greeting_special(name, keyword, is_special):
    response = get_greeting_special(name, keyword)
    assert response

    if not is_special:
        flag = True
        for val in SPECIAL_KEYWORDS_GREETING.values():
            if response in val:
                flag = False
        assert flag


def test_get_greeting_new_member():
    assert get_greeting_new_member("TestName")
