#
# test_slash_flashcard.py
#


import yaml
import warnings

from kotone.flashcard.init_flashcard import (
    _FLASHCARD_P_DRINKS,
    _FLASHCARD_P_ITEMS,
    _FLASHCARD_P_ITEMS_FREQ,
    _FLASHCARD_SKILLCARDS,
    _FLASHCARD_SKILLCARDS_FREQ,
)


def test_flashcard_p_drinks_yaml():
    with open("kotone/flashcard/flashcard_p_drinks.yaml", encoding="utf-8") as f:
        raw_flashcard = yaml.safe_load(f)

    assert isinstance(raw_flashcard, dict)
    assert isinstance(raw_flashcard.get("desc"), str)
    assert isinstance(raw_flashcard.get("content"), list)
    for item in raw_flashcard["content"]:
        assert isinstance(item, dict)
        assert isinstance(item.get("title"), str)
        assert isinstance(item.get("effect"), list)


def test_flashcard_p_items_yaml():
    with open("kotone/flashcard/flashcard_p_items.yaml", encoding="utf-8") as f:
        raw_flashcard = yaml.safe_load(f)

    assert isinstance(raw_flashcard, dict)
    assert isinstance(raw_flashcard.get("desc"), str)
    assert isinstance(raw_flashcard.get("content"), list)

    lst = raw_flashcard["content"]
    for i in range(len(lst)):
        item = lst[i]
        assert isinstance(item, dict)
        assert isinstance(item.get("title"), str)

        if item.get("is_enhanced") is False:
            assert item.get("title") == lst[i+1].get("title") and lst[i+1].get("is_enhanced")

        assert isinstance(item.get("effect"), list)


def test_flashcard_p_items_freq_yaml():
    with open("kotone/flashcard/flashcard_p_items_freq.yaml", encoding="utf-8") as f:
        freq_flashcard = yaml.safe_load(f)

    with open("kotone/flashcard/flashcard_p_items.yaml", encoding="utf-8") as f:
        full_flashcard = yaml.safe_load(f)

    assert isinstance(freq_flashcard, dict)
    assert isinstance(freq_flashcard.get("desc"), str)
    assert isinstance(freq_flashcard.get("content"), list)

    for title in freq_flashcard["content"]:
        assert isinstance(title, str)
        assert any(item["title"].startswith(title) for item in full_flashcard["content"])


def test_flashcard_skillcards_yaml():
    with open("kotone/flashcard/flashcard_skillcards.yaml", encoding="utf-8") as f:
        raw_flashcard = yaml.safe_load(f)

    assert isinstance(raw_flashcard, dict)
    assert isinstance(raw_flashcard.get("desc"), str)
    assert isinstance(raw_flashcard.get("content"), list)

    lst = raw_flashcard["content"]
    for i in range(len(lst)):
        item = lst[i]
        assert isinstance(item, dict)
        assert isinstance(item.get("title"), str)
        assert isinstance(item.get("skillcard_type"), str)

        if item.get("is_enhanced") is False:
            assert (
                item.get("title") == lst[i+1].get("title") and lst[i+1].get("is_enhanced")
                or item["skillcard_type"] == "T"
            )

        assert isinstance(item.get("cost"), dict)
        assert isinstance(item["cost"].get("val"), int)
        assert isinstance(item.get("effect"), list)

        if item["cost"].get("consumption_type"):
            assert isinstance(item["cost"]["consumption_type"], str)
            assert item["effect"][0].startswith( f"{ item["cost"]["consumption_type"] }消費{ abs(item["cost"]["val"]) }" )


def test_flashcard_skillcards_freq_yaml():
    with open("kotone/flashcard/flashcard_skillcards_freq.yaml", encoding="utf-8") as f:
        freq_flashcard = yaml.safe_load(f)

    with open("kotone/flashcard/flashcard_skillcards.yaml", encoding="utf-8") as f:
        full_flashcard = yaml.safe_load(f)

    assert isinstance(freq_flashcard, dict)
    assert isinstance(freq_flashcard.get("desc"), str)
    assert isinstance(freq_flashcard.get("content"), list)

    for title in freq_flashcard["content"]:
        assert isinstance(title, str)
        assert any(title in item["title"] for item in full_flashcard["content"])


def test_init_flashcard():
    for flashcard_dict in (
        _FLASHCARD_P_DRINKS,
        _FLASHCARD_P_ITEMS,
        _FLASHCARD_P_ITEMS_FREQ,
        _FLASHCARD_SKILLCARDS,
        _FLASHCARD_SKILLCARDS_FREQ,
    ):
        assert "desc" in flashcard_dict.keys()
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in flashcard_dict.items())


def test_flashcard_length():
    # Compare flashcard with the expected number of items currently in the game
    exp_num_p_drinks = 26
    exp_num_p_items = 187
    exp_num_skillcards = 139 * 2 + 1    # 228 * 2 + 1
    if len(_FLASHCARD_P_DRINKS.keys()) - 1 != exp_num_p_drinks:
        warnings.warn(UserWarning(f"Expected { exp_num_p_drinks } p-drinks in flashcard, instead found { len(_FLASHCARD_P_DRINKS.keys())-1 }"))
    if len(_FLASHCARD_P_ITEMS.keys()) - 1 != exp_num_p_items:
        warnings.warn(UserWarning(f"Expected { exp_num_p_items } p-items in flashcard, instead found { len(_FLASHCARD_P_ITEMS.keys())-1 }"))
    if len(_FLASHCARD_SKILLCARDS.keys()) - 1 != exp_num_skillcards:
        warnings.warn(UserWarning(f"Expected { exp_num_skillcards } skillcards in flashcard, instead found { len(_FLASHCARD_SKILLCARDS.keys())-1 }"))
