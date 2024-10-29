#
# utils/emoji.py
#


import random
from collections import ChainMap

KOTONE_EMOJI = {
    "KOTONE_1"   : "<:kotone1:1285561438651285545>",
    "KOTONE_2"   : "<:kotone2:1285561459715211316>",
    "KOTONE_HLW" : "<:kotone_hlw:1300558959802978357>",
    "MATANE"     : "<:matane:1300719633753571379>",
    "SITUREI"    : "<:siturei:1300725518307688458>",
}

P_ITEM_EMOJI = {
    "CHOKINBAKO" : "<:p_item_chokinbako:1285442904101490770>",
    "MINAMOTO"   : "<:p_item_minamoto:1285442926121586790>",
    "HANABI"     : "<:p_item_hanabi:1285442948133289984>",
}

IDOL_EMOJI = {
    "SAKI_1"     : "<:saki1:1285561319361220711>",
    "SAKI_2"     : "<:saki2:1285561340559360041>",
    "SAKI_HLW"   : "<:saki_hlw:1300558933118816386>",
    "OHAYOU"     : "<:ohayou:1300719573850656768>",
    "IIJANAI"    : "<:iijanai:1300725427123257374>",

    "TEMARI_1"   : "<:temari1:1285561361228632064>",
    "TEMARI_2"   : "<:temari2:1285561419424862208>",
    "TEMARI_HLW" : "<:temari_hlw:1300558949010903164>",
    "OTUKARESAMA": "<:otukaresama:1300719585024020530>",
    "EE"         : "<:ee:1300725450699575316>",

    "KOTONE_1"   : "<:kotone1:1285561438651285545>",
    "KOTONE_2"   : "<:kotone2:1285561459715211316>",
    "KOTONE_HLW" : "<:kotone_hlw:1300558959802978357>",
    "MATANE"     : "<:matane:1300719633753571379>",
    "SITUREI"    : "<:siturei:1300725518307688458>",

    "MAO_1"      : "<:mao1:1285561485216710657>",
    "MAO_2"      : "<:mao2:1285561501478027334>",
    "MAO_HLW"    : "<:mao_hlw:1300558972276707358>",
    "MAKASETE"   : "<:makasete:1300719647670140940>",
    "MATTAKU"    : "<:mattaku:1300725529925648424>",

    "LILJA_1"    : "<:lilja1:1285561516221005864>",
    "LILJA_2"    : "<:lilja2:1285561530494091274>",
    "LILJA_HLW"  : "<:lilja_hlw:1300558985593622558>",
    "GOMENNASAI" : "<:gomennasai:1300719658151968769>",
    "QUES"       : "<:ques:1300725542819201045>",

    "CHINA_1"    : "<:china1:1285561540887580715>",
    "CHINA_2"    : "<:china2:1285561553827008614>",
    "CHINA_HLW"  : "<:china_hlw:1300558996876562503>",
    "DESUWA"     : "<:desuwa:1300719665034694666>",
    "MAA"        : "<:maa:1300725555666092084>",

    "SUMIKA_1"   : "<:sumika1:1285561562840432640>",
    "SUMIKA_2"   : "<:sumika2:1285561582402932838>",
    "SUMIKA_HLW" : "<:sumika_hlw:1300559011560685638>",
    "YOROSIKU"   : "<:yorosiku:1300719676174893057>",
    "UKERU"      : "<:ukeru:1300725585273815040>",

    "HIRO_1"     : "<:hiro1:1285561593916166155>",
    "HIRO_2"     : "<:hiro2:1285561607522357339>",
    "HIRO_HLW"   : "<:hiro_hlw:1300559043047194655>",
    "DAIJOUBU"   : "<:daijoubu:1300719686157078529>",
    "HETOHETO"   : "<:hetoheto:1300725598892855317>",

    "UME_1"      : "<:ume1:1285561636937007127>",
    "UME_2"      : "<:ume2:1285561659003502606>",
    "UME_HLW"    : "<:ume_hlw:1300559058746474547>",
    "YATTA"      : "<:yatta:1300719697305800774>",
    "GOKUGOKU"   : "<:gokugoku:1300725612352245760>",

    "MISUZU_1"   : "<:misuzu1:1300557160341569568>",
    "MISUZU_2"   : "<:misuzu2:1300557185167655195>",
    "MISUZU_HLW" : "<:misuzu_hlw:1300559069723099137>",
    "YASUMIMASYO": "<:yasumimasyo:1300719706155782196>",
    "OYASUMI"    : "<:oyasumi:1300725625270829066>",

    "SENA_1"     : "<:sena1:1300557205904429128>",
    "SENA_2"     : "<:sena2:1300557223319044176>",
    "SENA_HLW"   : "<:sena_hlw:1300559085359464530>",
    "ARIGATOU"   : "<:arigatou:1300719718554144778>",
    "HUMU"       : "<:humu:1300725645915197481>",

    "RINAMI_1"   : "<:rinami1:1285561615353380896>",
    "RINAMI_2"   : "<:rinami2:1285561627877576724>",
    "RINAMI_HLW" : "<:rinami_hlw:1300559180863897650>",
    "OMEDETOU"   : "<:omedetou:1300719732391018496>",
    "NEENEE"     : "<:neenee:1300725658724339742>",

    "WAKARIMASITAKA": "<:wakarimasitaka:1300725679238807624>",
    "POINT"         : "<:point:1300725693034004502>",
    "GANBATTANA"    : "<:ganbattana:1300725722129760266>",
    "SUGOIWA"       : "<:sugoiwa:1300725731973926942>",
    "HAJIMEMASUNE"  : "<:hajimemasune:1300725746729222206>",
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


if __name__ == "__main__":
    print("Examples of emoji:")
    print(get_emoji())
    print(get_emoji(KOTONE_EMOJI))
    print(get_emoji(P_ITEM_EMOJI))
    print(get_emoji(KOTONE_EMOJI, P_ITEM_EMOJI))
