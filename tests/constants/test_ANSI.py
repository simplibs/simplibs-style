import re

import pytest
# Outers
from simplibs.style.constants import ANSI


# The table is written out by hand from the ANSI standard, not built from
# the code under test, so a wrong value in ANSI.py cannot hide itself.
EXPECTED: dict[str, str] = {
    "RESET": "0",
    # Text attributes
    "BOLD": "1",
    "DIM": "2",
    "ITALIC": "3",
    "UNDERLINE": "4",
    "BLINK": "5",
    "BLINK_FAST": "6",
    "REVERSE": "7",
    "HIDDEN": "8",
    "STRIKETHROUGH": "9",
    # Attributes off
    "BOLD_OFF": "22",
    "DIM_OFF": "22",
    "ITALIC_OFF": "23",
    "UNDERLINE_OFF": "24",
    "BLINK_OFF": "25",
    "REVERSE_OFF": "27",
    "HIDDEN_OFF": "28",
    "STRIKETHROUGH_OFF": "29",
    # Foreground, standard
    "FG_BLACK": "30",
    "FG_RED": "31",
    "FG_GREEN": "32",
    "FG_YELLOW": "33",
    "FG_BLUE": "34",
    "FG_MAGENTA": "35",
    "FG_CYAN": "36",
    "FG_WHITE": "37",
    "FG_DEFAULT": "39",
    # Background, standard
    "BG_BLACK": "40",
    "BG_RED": "41",
    "BG_GREEN": "42",
    "BG_YELLOW": "43",
    "BG_BLUE": "44",
    "BG_MAGENTA": "45",
    "BG_CYAN": "46",
    "BG_WHITE": "47",
    "BG_DEFAULT": "49",
    # Foreground, bright
    "FG_BRIGHT_BLACK": "90",
    "FG_BRIGHT_RED": "91",
    "FG_BRIGHT_GREEN": "92",
    "FG_BRIGHT_YELLOW": "93",
    "FG_BRIGHT_BLUE": "94",
    "FG_BRIGHT_MAGENTA": "95",
    "FG_BRIGHT_CYAN": "96",
    "FG_BRIGHT_WHITE": "97",
    # Background, bright
    "BG_BRIGHT_BLACK": "100",
    "BG_BRIGHT_RED": "101",
    "BG_BRIGHT_GREEN": "102",
    "BG_BRIGHT_YELLOW": "103",
    "BG_BRIGHT_BLUE": "104",
    "BG_BRIGHT_MAGENTA": "105",
    "BG_BRIGHT_CYAN": "106",
    "BG_BRIGHT_WHITE": "107",
    # Extended colors
    "FG_EXTENDED": "38",
    "BG_EXTENDED": "48",
    "EXTENDED_256": "5",
    "EXTENDED_RGB": "2",
}

COLORS = ("BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE")


def public_table() -> dict[str, str]:
    """Every public name of the ANSI module with its value."""
    return {name: value for name, value in vars(ANSI).items() if not name.startswith("_")}


# ----------------------------------------------------------------------
# The table as a whole
# ----------------------------------------------------------------------
def test_table_holds_exactly_the_expected_names() -> None:
    assert set(public_table()) == set(EXPECTED)


@pytest.mark.parametrize("name, expected", list(EXPECTED.items()))
def test_every_code_has_its_standard_value(name: str, expected: str) -> None:
    assert getattr(ANSI, name) == expected


def test_every_value_is_a_string_of_ascii_digits() -> None:
    for name, value in public_table().items():
        assert isinstance(value, str), name
        assert re.fullmatch(r"[0-9]+", value), name


def test_every_name_is_uppercase() -> None:
    for name in public_table():
        assert name == name.upper(), name


# ----------------------------------------------------------------------
# Values that several names share
# ----------------------------------------------------------------------
def test_only_known_names_share_a_value() -> None:
    groups: dict[str, set[str]] = {}
    for name, value in public_table().items():
        groups.setdefault(value, set()).add(name)

    shared = {value: names for value, names in groups.items() if len(names) > 1}

    assert shared == {
        # Bold and dim have one common "off" code
        "22": {"BOLD_OFF", "DIM_OFF"},
        # "5" and "2" follow 38/48 as the kind of color; elsewhere they are attributes
        "5": {"BLINK", "EXTENDED_256"},
        "2": {"DIM", "EXTENDED_RGB"},
    }


def test_bold_off_is_not_21() -> None:
    # "21" is read as double underline by many terminals
    assert ANSI.BOLD_OFF != "21"
    assert ANSI.BOLD_OFF == ANSI.DIM_OFF == "22"


# ----------------------------------------------------------------------
# The color families follow the order of the standard
# ----------------------------------------------------------------------
@pytest.mark.parametrize("index, color", list(enumerate(COLORS)))
def test_color_families_are_consecutive(index: int, color: str) -> None:
    assert getattr(ANSI, f"FG_{color}") == str(30 + index)
    assert getattr(ANSI, f"BG_{color}") == str(40 + index)
    assert getattr(ANSI, f"FG_BRIGHT_{color}") == str(90 + index)
    assert getattr(ANSI, f"BG_BRIGHT_{color}") == str(100 + index)
