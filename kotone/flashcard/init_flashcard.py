#
# init_flashcard.py
#


import importlib.resources
import kotone.flashcard
import yaml
from typing import Any, Optional


def _parse_flashcard(raw_flashcard: dict[str, Any]) -> dict[str, str]:
    """ Converts texts in `raw_flashcard` into Discord-styled
        messages to be used by `slash_flashcard.py`.
        The resulting dict contains a `"desc"` key-value
        while other items are keyed by title.

        `raw_flashcard` must contain keys `"desc"` and `"content"`.
    """
    result = {"desc": raw_flashcard["desc"]}
    for item in raw_flashcard["content"]:
        title = _parse_title(item["title"], item.get("skillcard_type"), item.get("is_enhanced"), item.get("cost"), item.get("origin"))
        effect = _parse_effect(item["effect"])
        result[title] = effect
    return result


def _parse_title(
    title: str,
    skillcard_type: Optional[str],
    is_enhanced: Optional[bool],
    cost: Optional[dict[str, str]],
    origin: Optional[dict[str, str]],
) -> str:
    """ Helper function to parse an item's title. """
    if skillcard_type:
        title = f"({ skillcard_type }) { title }"

    if is_enhanced:
        title += "+"

    if cost:
        title += f" { cost.get("consumption_type") or "♡" }{ cost["val"] }"

    if origin:
        if origin.get("idol"):
            title += f" ([{ origin["card_name"] }]{ origin["idol"] })"
        else:
            title += f" ({ origin["card_name"] })"

    return title


def _parse_effect(effect_lst: list[str]) -> str:
    """ Helper function to parse an item's effect. """
    return "\n".join("* " + effect for effect in effect_lst)


def _parse_flashcard_freq(
    raw_flashcard_freq: dict[str, Any],
    full_flashcard: dict[str, str],
    exclude_origin_nonenhanced: bool,
) -> dict[str, str]:
    """ Returns a partial flashcard dict from `full_flashcard`
        containing only items specified by `raw_flashcard_freq`.

        Intended for cutting down the size of flashcards
        so they only contain frequently-used items.

        If `exclude_origin_nonenhanced`, this excludes
        non-enhanced versions of produce skillcards.
    """
    result = {"desc": raw_flashcard_freq["desc"]}
    title_list = raw_flashcard_freq["content"]

    for key in full_flashcard.keys() - {"desc"}:
        if any(title in key for title in title_list):
            # Exclude non-enhanced version of produce skillcards
            if (
                exclude_origin_nonenhanced
                and "]" in key
                and ")" in key
                and "+ ([" not in key
            ):
                continue

            result[key] = full_flashcard[key]

    return result


# Load and parse flashcards from .yaml
resource = importlib.resources.files(kotone.flashcard)


with resource.joinpath("flashcard_p_drinks.yaml").open(encoding="utf-8") as f:
    _raw_p_drinks = yaml.safe_load(f)
_FLASHCARD_P_DRINKS = _parse_flashcard(_raw_p_drinks)


with resource.joinpath("flashcard_p_items.yaml").open(encoding="utf-8") as f:
    _raw_p_items = yaml.safe_load(f)
_FLASHCARD_P_ITEMS = _parse_flashcard(_raw_p_items)


with resource.joinpath("flashcard_p_items_freq.yaml").open(encoding="utf-8") as f:
    _raw_p_items_freq = yaml.safe_load(f)
_FLASHCARD_P_ITEMS_FREQ = _parse_flashcard_freq(_raw_p_items_freq, _FLASHCARD_P_ITEMS, False)


with resource.joinpath("flashcard_skillcards.yaml").open(encoding="utf-8") as f:
    _raw_skillcards = yaml.safe_load(f)
_FLASHCARD_SKILLCARDS = _parse_flashcard(_raw_skillcards)


with resource.joinpath("flashcard_skillcards_freq.yaml").open(encoding="utf-8") as f:
    _raw_skillcards_freq = yaml.safe_load(f)
_FLASHCARD_SKILLCARDS_FREQ = _parse_flashcard_freq(_raw_skillcards_freq, _FLASHCARD_SKILLCARDS, True)
