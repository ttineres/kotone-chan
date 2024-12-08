#
# voiceline.py
#


from datetime import datetime, timezone, timedelta
import random
import logging


HOME_VOICE = {
    "HOME_1"  : "あの……忙しそうですけど、ちゃんと休んでます？",
    "HOME_2"  : "少しでも稼ぐ！　これは譲れません！",
    "HOME_3"  : "明日はボーカルレッスンかぁ……頑張りますっ。",
    "HOME_4"  : "目指せ大金持ち！！　……聞いちゃいましたぁ？",
    "HOME_5"  : "実は会長のこと、ちょっぴり苦手なんですよね……",
    "HOME_6"  : "最後まで、ちゃんと面倒を見てくださいね！",
    "HOME_7"  : "可愛さの秘訣はですねぇ……秘密でーす♡",
    "HOME_8"  : "子供の相手は得意なんです。家で慣れてますから。",
    "HOME_9"  : "はーい。呼びました？",
    "HOME_10" : "……もしかして、お仕事の話ですか！？",
    "HOME_11" : "一緒にお話しちゃいます？",
    "HOME_12" : "これまでのことですかぁ？　大したこと話せませんけどぉ。",
    "HOME_13" : "張り切っていきましょう～！",
    "HOME_14" : "あたしが一番可愛いですよね！",
    "HOME_15" : "そんなにあたしのこと気になります？",
    "HOME_16" : "少しは成績上がってますかね……",
    "HOME_17" : "はっきり言ってくれないと、メッチャ怖いんですけどォ！！",
    "HOME_18" : "ナ～あたしのこと好きすぎでしょ♡",
}


_JAPAN_TIMEZONE = timezone(timedelta(hours=9))


def get_greeting(name: str) -> str:
    """ Randomly generates greeting for user with `name`. """
    rand = random.random()
    if rand < 0.1:
        return get_aisatu(name)
    if rand < 0.2:
        return get_season_aisatu(name)
    random_key = random.choice([*HOME_VOICE.keys()])
    return HOME_VOICE[random_key]


def get_aisatu(name: str) -> str:
    """ Returns greeting that changes based on the time of day. """
    now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(_JAPAN_TIMEZONE)

    if 6 <= now.hour < 11:
        return random.choice([
            f"おっはようございまーす、{name}さん！",
            "今日も一日頑張りましょう！",
        ])
    if 11 <= now.hour < 14:
        return random.choice([
            f"どーも！　{name}さんもお昼です？",
            "お弁当で元気チャージしてぇ、午後も頑張りまーす！",
        ])
    if 14 <= now.hour < 18:
        return random.choice([
            "さてさて、こっからが本番ですよね！",
            "可愛いことねちゃんとの時間が始まりますよぉ～",
        ])
    else:
        return random.choice([
            "お疲れさまでーす！",
            "今日も後ちょっと、頑張りましょう！"
        ])


def get_season_aisatu(name: str) -> str:
    """ Returns greeting that changes based on season. """
    now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(_JAPAN_TIMEZONE)
    if 3 <= now.month < 6:
        return random.choice([
            "来ました……春限定メニューという名の、繁忙期がぁ～！",
            f"{name}さん、お花見いきましょうよ～",
            "もう外でレッスンしても、寒くなさそうですね！",
        ])
    if 6 <= now.month < 9:
        return random.choice([
            f"{name}さん、もっと冷房強くなんないんですか～？",
            "真夏の着ぐるみバイト……さすがに……",
            "最近、チビ共が海行きたい～って、うるさいんですよ。",
        ])
    if 9 <= now.month < 12:
        return random.choice([
            "フルーツ狩りって、いくつ取れたらお得なんですかね……",
            "働きやすい気温になってきましたね！",
            f"{name}さん！　お仕事の秋が来ましたよ！",
        ])
    else:
        return random.choice([
            "寒いからって、外でのお仕事を減らしちゃだめですよ！",
            f"{name}さん、あったかい衣装くーださい♪",
            f"風邪にお気をつけてくださいね？",
        ])


def get_greeting_new_member(name: str) -> str:
    """ Generates greeting for new member with `name`. """
    return random.choice([
        f"ようこそ、{name}さん！　ここで素敵な時間を過ごしましょう～～！",
        f"{name}さん、いらっしゃい～♪",
        f"{name}さん、ようこそ！　どうぞよろしくお願いしまぁーす。",
        f"{name}さん、あたしたちのサーバーへようこそ！",
        f"{name}さん、よろ～。",
        f"いらっしゃい、{name}さん！　これから一緒に頑張りましょうね！",
        f"あ、{name}さん、いらっしゃい！",
        f"ようこそ、{name}さん！　サーバーの一員として楽しんでね！",
        f"{name}さん、ようこそ！　素敵な仲間が増えましたね♪",
        f"{name}さん、よろ～。",
    ])


SPECIAL_KEYWORDS_GREETING = {
    "奇遇ね": [
        "げっ！　どうしてこんなとこまでッ！？",
        "うぇっ。な、なんすか？",
        "げっ……しっつれいしまぁーす！",
        "うぇっ！　勘弁してくださぁ～い！",
        "げっ！　なんでいるんだよ！",
        "うげっ！　……会長かと思いましたぁ。",
        "じゅ、十王会長！？",
        "会長！？　とっ……とりあえず――場所！　場所変えましょう！！",
        "お、オハヨ～ございまぁす。",
        "……え……十王会長！？",
    ],
    "ママうるさい": [
        "う……ん……ん゛～～……くるしぃ……おもぉい。",
        "おっ……おーまーえーらぁ～～～～～～～～～～！！",
        "ここ、あたしの布団！　寝苦しいと思ったらさぁ～！",
        "なんで領土侵犯してくんの！？　寝相悪すぎぃ！",
        "ママじゃねーんだよぉ！",
        "さっさと起きてどけぇ～！",
        "やっぱあたし、おまえらのことキライだわ！",
    ]
}


def get_greeting_special(name: str, keyword: str) -> str:
    """ Greets user with respect to the invoked special `keyword`.

        `keyword` should be a key in `SPECIAL_KEYWORDS_GREETING` dict.
    """
    if keyword in SPECIAL_KEYWORDS_GREETING.keys():
        return random.choice(SPECIAL_KEYWORDS_GREETING[keyword])
    else:
        logging.info(f"[KOTONE] Could not properly call get_greeting_special({keyword}, {name}). This condition is caused by a bug in the kotone package.")
        return get_greeting(name)
