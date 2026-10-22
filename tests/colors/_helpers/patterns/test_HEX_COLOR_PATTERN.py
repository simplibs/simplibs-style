import re

import pytest
# Outers
from simplibs.style.colors._helpers.patterns import HEX_COLOR_PATTERN


# (text, the digits of group 1)
VALID = [
    ("#ff8800", "ff8800"),
    ("ff8800", "ff8800"),
    ("#f80", "f80"),
    ("f80", "f80"),
    ("#FF8800", "FF8800"),
    ("#aBc123", "aBc123"),
    ("#000", "000"),
    ("#ffffff", "ffffff"),
]

INVALID = [
    "",
    "#",
    # Wrong number of digits
    "#f",
    "#ff",
    "#ffff",
    "#fffff",
    "#fffffff",
    "#ffff00ff",
    # Not hex digits
    "#gg8800",
    "#ff88zz",
    # Extra characters around or inside
    " ff8800",
    "ff8800 ",
    "ff8800\n",
    "ff 8800",
    "##ff8800",
    "0xff8800",
    "rgb(1,2,3)",
    "orange",
    # Digits that are not ASCII
    "#ff88０0",
    "ＦＦ８８００",
]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(HEX_COLOR_PATTERN, re.Pattern)


@pytest.mark.parametrize("text, digits", VALID)
def test_accepts_a_hex_color_and_captures_the_digits(text: str, digits: str) -> None:
    match = HEX_COLOR_PATTERN.fullmatch(text)

    assert match is not None
    assert match.group(1) == digits


@pytest.mark.parametrize("text", INVALID)
def test_refuses_everything_else(text: str) -> None:
    assert HEX_COLOR_PATTERN.fullmatch(text) is None
