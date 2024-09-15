#
# voice.py
#


from datetime import datetime, timezone
import random


HOME_1 = "あの……忙しそうですけど、ちゃんと休んでます？"
HOME_2 = "少しでも稼ぐ！　これは譲れません！"
HOME_3 = "明日はボーカルレッスンかぁ……頑張りますっ。"
HOME_4 = "目指せ大金持ち！！　……聞いちゃいましたぁ？"
HOME_5 = "実は会長のこと、ちょっぴり苦手なんですよね……"
HOME_6 = "最後まで、ちゃんと面倒を見てくださいね！"
HOME_7 = "可愛さの秘訣はですねぇ……秘密でーす♡"
HOME_8 = "子供の相手は得意なんです。家で慣れてますから。"
HOME_9 = "はーい。呼びました？"
HOME_10 = "……もしかして、お仕事の話ですか！？"
HOME_11 = "一緒にお話しちゃいます？"
HOME_12 = "これまでのことですかぁ？　大したこと話せませんけどぉ。"
HOME_13 = "張り切っていきましょう～！"
HOME_14 = "あたしが一番可愛いですよね！"
HOME_15 = "そんなにあたしのこと気になります？"
HOME_16 = "少しは成績上がってますかね……"
HOME_17 = "はっきり言ってくれないと、メッチャ怖いんですけどォ！！"
HOME_18 = "ナ～あたしのこと好きすぎでしょ♡"

HOME_VOICE = [
    HOME_1,
    HOME_2,
    HOME_3,
    HOME_4,
    HOME_5,
    HOME_6,
    HOME_7,
    HOME_8,
    HOME_9,
    HOME_10,
    HOME_11,
    HOME_12,
    HOME_13,
    HOME_14,
    HOME_15,
    HOME_16,
    HOME_17,
    HOME_18,
]

def greeting(name):
    """ Randomly generates greeting. """
    rand = random.random()
    if rand < 0.1:
        return aisatu(name)
    if rand < 0.2:
        return season_aisatu(name)
    return random.choice(HOME_VOICE)

def aisatu(name):
    """ Returns greeting that changes based on the time of day. """
    now = datetime.now(timezone.utc)
    if 21 <= now.hour or now.hour < 2:
        return random.choice([
            f"おっはようございまーす、{name}さん！",
            "今日も一日頑張りましょう！",
        ])
    if 2 <= now.hour < 5:
        return random.choice([
            f"どーも！　{name}さんもお昼です？",
            "お弁当で元気チャージしてぇ、午後も頑張りまーす！",
        ])
    if 5 <= now.hour < 9:
        return random.choice([
            "さてさて、こっからが本番ですよね！",
            "可愛いことねちゃんとの時間が始まりますよぉ～",
        ])
    else:
        return random.choice([
            "お疲れさまでーす！",
            "今日も後ちょっと、頑張りましょう！"
        ])

def season_aisatu(name):
    """ Returns greeting that changes based on season. """
    now = datetime.now(timezone.utc)
    if now.month <= 3:
        return random.choice([
            "来ました……春限定メニューという名の、繁忙期がぁ～！",
            f"{name}さん、お花見いきましょうよ～",
            "もう外でレッスンしても、寒くなさそうですね！",
        ])
    if now.month <= 6:
        return random.choice([
            f"{name}さん、もっと冷房強くなんないんですか～？",
            "真夏の着ぐるみバイト……さすがに……",
            "最近、チビ共が海行きたい～って、うるさいんですよ。",
        ])
    else:
        return random.choice([
            "フルーツ狩りって、いくつ取れたらお得なんですかね……",
            "働きやすい気温になってきましたね！",
            f"{name}さん！　お仕事の秋が来ましたよ！"
        ])
