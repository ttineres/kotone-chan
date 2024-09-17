#
# voice.py
#


from datetime import datetime, timezone, timedelta
import random


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

JAPAN_TIMEZONE = timezone(timedelta(hours=9))

def get_greeting(name):
    """ Randomly generates greeting. """
    rand = random.random()
    if rand < 0.1:
        return get_aisatu(name)
    if rand < 0.2:
        return get_season_aisatu(name)
    random_key = random.choice([*HOME_VOICE.keys()])
    return HOME_VOICE[random_key]

def get_aisatu(name):
    """ Returns greeting that changes based on the time of day. """
    now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(JAPAN_TIMEZONE)
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

def get_season_aisatu(name):
    """ Returns greeting that changes based on season. """
    now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).astimezone(JAPAN_TIMEZONE)
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
    else:
        return random.choice([
            "フルーツ狩りって、いくつ取れたらお得なんですかね……",
            "働きやすい気温になってきましたね！",
            f"{name}さん！　お仕事の秋が来ましたよ！"
        ])

def get_greeting_new_member(name):
    """ Generates greeting for new member. """
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


SPECIAL_KEYWORDS_GREETING = [
    "奇遇ね",
]

def get_greeting_special(name, keyword):
    """ Greets user if special keyword is used.
        Input keyword should be a member of SPECIAL_KEYWORDS_GREETING.
    """
    match keyword:
        case "奇遇ね":
            return random.choice([
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
            ])
        case _:
            print(f"[KOTONE] Could not properly call get_greeting_special({keyword}, {name}).")
            return get_greeting(name)


if __name__ == "__main__":
    print("Examples of greeting:")
    print(get_greeting("username"))
    print(get_greeting("username"))
    print(get_greeting("username"))
    print(get_greeting("username"))
    print(get_greeting("username"))
    print(get_greeting("username"))
    print("Examples of greeting new member:")
    print(get_greeting_new_member("username"))
    print(get_greeting_new_member("username"))
    print(get_greeting_new_member("username"))
    print(get_greeting_new_member("username"))
    print(get_greeting_new_member("username"))
    print(get_greeting_new_member("username"))
    print("Examples of special greeting:")
    print(get_greeting_special("username"))
    print(get_greeting_special("username"))
