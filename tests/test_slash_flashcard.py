#
# test_slash_flashcard.py
#


import yaml


# Test .yaml files
with open("flashcard_p_drinks.yaml", encoding="utf-8") as f:
    data = yaml.safe_load(f)

assert isinstance(data, dict)
assert data.get("desc")
assert data.get("content")
for item in data.get("content"):
    assert item.get("title")
    assert item.get("effect")
    assert isinstance(item.get("effect"), list)


with open("flashcard_p_items.yaml", encoding="utf-8") as f:
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
