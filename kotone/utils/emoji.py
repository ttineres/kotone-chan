#
# utils/emoji.py
#


import random
from collections import ChainMap

KOTONE_EMOJI = {
    "KOTONE_1": "<:kotone1:1284666285476675604>",
    "KOTONE_2": "<:kotone2:1284666311737344043>",
    "MATANE"  : "<:matane:1284666329839698051>",
    "SITUREI" : "<:siturei:1284666348374593619>",
}

P_ITEM_EMOJI = {
    "CHOKINBAKO": "<:p_item_chokinbako:1285442904101490770>",
    "MINAMOTO": "<:p_item_minamoto:1285442926121586790>",
    "HANABI": "<:p_item_hanabi:1285442948133289984>",
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
