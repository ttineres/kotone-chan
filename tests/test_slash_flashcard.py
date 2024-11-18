#
# test_slash_flashcard.py
#


import yaml

from kotone.flashcard.init_flashcard import (
    _FLASHCARD_P_DRINKS,
    _FLASHCARD_P_ITEMS,
    _FLASHCARD_P_ITEMS_FREQ,
)


def test_yaml_files():
    with open("kotone/flashcard/flashcard_p_drinks.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict)
    assert data.get("desc")
    assert data.get("content")
    for item in data.get("content"):
        assert item.get("title")
        assert item.get("effect")
        assert isinstance(item.get("effect"), list)

    with open("kotone/flashcard/flashcard_p_items.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict)
    assert data.get("desc")
    assert data.get("content")
    lst = data.get("content")
    for i in range(len(lst)):
        item = lst[i]
        assert item.get("title")
        if item.get("is_enhanced") is False:
            assert item.get("title") == lst[i+1].get("title") and lst[i+1].get("is_enhanced")
        assert item.get("effect")
        assert isinstance(item.get("effect"), list)

    with open("kotone/flashcard/flashcard_p_items_freq.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict)
    assert data.get("desc")
    assert data.get("content")


def test_init_flashcard():
    for flashcard_dict in (
        _FLASHCARD_P_DRINKS,
        _FLASHCARD_P_ITEMS,
        _FLASHCARD_P_ITEMS_FREQ,
    ):
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in flashcard_dict.items())
