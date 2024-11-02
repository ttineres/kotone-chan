#
# utils/emoji.py
#


import random
from collections import ChainMap
import re

KOTONE_EMOJI = {
    "kotone1"    : "<:kotone1:1285561438651285545>",
    "kotone2"    : "<:kotone2:1285561459715211316>",
    "kotone_hlw" : "<:kotone_hlw:1300558959802978357>",
    "matane"     : "<:matane:1300719633753571379>",
    "siturei"    : "<:siturei:1300725518307688458>",
}

P_ITEM_EMOJI = {
    "p_item_chokinbako": "<:p_item_chokinbako:1285442904101490770>",
    "p_item_minamoto"  : "<:p_item_minamoto:1285442926121586790>",
    "p_item_hanabi"    : "<:p_item_hanabi:1285442948133289984>",
}

IDOL_EMOJI = {
    "saki1"      : "<:saki1:1285561319361220711>",
    "saki2"      : "<:saki2:1285561340559360041>",
    "saki_hlw"   : "<:saki_hlw:1300558933118816386>",
    "ohayou"     : "<:ohayou:1300719573850656768>",
    "iijanai"    : "<:iijanai:1300725427123257374>",

    "temari1"    : "<:temari1:1285561361228632064>",
    "temari2"    : "<:temari2:1285561419424862208>",
    "temari_hlw" : "<:temari_hlw:1300558949010903164>",
    "otukaresama": "<:otukaresama:1300719585024020530>",
    "ee"         : "<:ee:1300725450699575316>",

    "kotone1"    : "<:kotone1:1285561438651285545>",
    "kotone2"    : "<:kotone2:1285561459715211316>",
    "kotone_hlw" : "<:kotone_hlw:1300558959802978357>",
    "matane"     : "<:matane:1300719633753571379>",
    "siturei"    : "<:siturei:1300725518307688458>",

    "mao1"       : "<:mao1:1285561485216710657>",
    "mao2"       : "<:mao2:1285561501478027334>",
    "mao_hlw"    : "<:mao_hlw:1300558972276707358>",
    "makasete"   : "<:makasete:1300719647670140940>",
    "mattaku"    : "<:mattaku:1300725529925648424>",

    "lilja1"     : "<:lilja1:1285561516221005864>",
    "lilja2"     : "<:lilja2:1285561530494091274>",
    "lilja_hlw"  : "<:lilja_hlw:1300558985593622558>",
    "gomennasai" : "<:gomennasai:1300719658151968769>",
    "ques"       : "<:ques:1300725542819201045>",

    "china1"     : "<:china1:1285561540887580715>",
    "china2"     : "<:china2:1285561553827008614>",
    "china_hlw"  : "<:china_hlw:1300558996876562503>",
    "desuwa"     : "<:desuwa:1300719665034694666>",
    "maa"        : "<:maa:1300725555666092084>",

    "sumika1"    : "<:sumika1:1285561562840432640>",
    "sumika2"    : "<:sumika2:1285561582402932838>",
    "sumika_hlw" : "<:sumika_hlw:1300559011560685638>",
    "yorosiku"   : "<:yorosiku:1300719676174893057>",
    "ukeru"      : "<:ukeru:1300725585273815040>",

    "hiro1"      : "<:hiro1:1285561593916166155>",
    "hiro2"      : "<:hiro2:1285561607522357339>",
    "hiro_hlw"   : "<:hiro_hlw:1300559043047194655>",
    "daijoubu"   : "<:daijoubu:1300719686157078529>",
    "hetoheto"   : "<:hetoheto:1300725598892855317>",

    "ume1"       : "<:ume1:1285561636937007127>",
    "ume2"       : "<:ume2:1285561659003502606>",
    "ume_hlw"    : "<:ume_hlw:1300559058746474547>",
    "yatta"      : "<:yatta:1300719697305800774>",
    "gokugoku"   : "<:gokugoku:1300725612352245760>",

    "misuzu1"    : "<:misuzu1:1300557160341569568>",
    "misuzu2"    : "<:misuzu2:1300557185167655195>",
    "misuzu_hlw" : "<:misuzu_hlw:1300559069723099137>",
    "yasumimasyo": "<:yasumimasyo:1300719706155782196>",
    "oyasumi"    : "<:oyasumi:1300725625270829066>",

    "sena1"      : "<:sena1:1300557205904429128>",
    "sena2"      : "<:sena2:1300557223319044176>",
    "sena_hlw"   : "<:sena_hlw:1300559085359464530>",
    "arigatou"   : "<:arigatou:1300719718554144778>",
    "humu"       : "<:humu:1300725645915197481>",

    "rinami1"    : "<:rinami1:1285561615353380896>",
    "rinami2"    : "<:rinami2:1285561627877576724>",
    "rinami_hlw" : "<:rinami_hlw:1300559180863897650>",
    "omedetou"   : "<:omedetou:1300719732391018496>",
    "neenee"     : "<:neenee:1300725658724339742>",

    "wakarimasitaka": "<:wakarimasitaka:1300725679238807624>",
    "point"         : "<:point:1300725693034004502>",
    "ganbattana"    : "<:ganbattana:1300725722129760266>",
    "sugoiwa"       : "<:sugoiwa:1300725731973926942>",
    "hajimemasune"  : "<:hajimemasune:1300725746729222206>",
}

def get_emoji(*emoji_dicts):
    """ Returns a random emoji chosen from all emoji dicts.
        Specify emoji_dicts to choose only from those dicts.
    """
    emojis = {}
    if emoji_dicts:
        emojis = dict(ChainMap(*emoji_dicts))
    else:
        emojis = {**KOTONE_EMOJI, **P_ITEM_EMOJI}
    random_key = random.choice([*emojis.keys()])
    return emojis[random_key]

def replace_match(match):
    """ Helper function for replace_idol_emoji(). """
    emoji_name = match.group(1)
    return IDOL_EMOJI.get(emoji_name, match.group(0))

def replace_idol_emoji(message):
    """ Replaces all instances of idol emojis formatted
        as :emoji_name: with appropriate values in IDOL_EMOJI.
    """
    # Regular expression to match Discord emoji syntax
    emoji_pattern = r"<:(\w+):\d+>"

    # Replace appropriate idol emojis
    new_message = re.sub(emoji_pattern, replace_match, message)

    return new_message


if __name__ == "__main__":
    print("Examples of emoji:")
    print(get_emoji())
    print(get_emoji(KOTONE_EMOJI))
    print(get_emoji(P_ITEM_EMOJI))
    print(get_emoji(KOTONE_EMOJI, P_ITEM_EMOJI))
    print("Examples of messages with replaced idol emojis:")
    print(replace_idol_emoji("手毬<:temari1:1240868706989641738>"))
    print(replace_idol_emoji(
        "俺<:TheTman:467927310184611841>:"
        "今日は<:ques:1247745906816585729>なんだ"
    ))
    print(replace_idol_emoji(
        ":happy::lucky:<:wakarimasitaka:1247746311252480070> "
        "<:character_150KingBoo:1084132570020720701>"
    ))
