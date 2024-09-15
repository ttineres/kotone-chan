#
# emoji.py
#


import random


KOTONE_EMOJI = {
    "KOTONE_1": "<:kotone1:1284666285476675604>",
    "KOTONE_2": "<:kotone2:1284666311737344043>",
    "MATANE"  : "<:matane:1284666329839698051>",
    "SITUREI" : "<:siturei:1284666348374593619>",
}

def get_kotone():
    """ Returns a random Kotone emoji. """
    random_key = random.choice([*KOTONE_EMOJI.keys()])
    return KOTONE_EMOJI[random_key]

# Previous implementation of emoji
"""
KOTONE_1 = "<:kotone1:1284666285476675604>"
KOTONE_2 = "<:kotone2:1284666311737344043>"
MATANE   = "<:matane:1284666329839698051>"
SITUREI  = "<:siturei:1284666348374593619>"
KOTONE = [
    KOTONE_1,
    KOTONE_2,
    MATANE,
    SITUREI,
]
"""


if __name__ == "__main__":
    print("Examples of emoji:")
    print(get_kotone())
    print(get_kotone())
    print(get_kotone())
