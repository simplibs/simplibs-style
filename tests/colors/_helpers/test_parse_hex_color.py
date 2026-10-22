import pytest
# Outers
from simplibs.style.colors._helpers import parse_hex_color


# (text, the channels)
PARSED = [
    # Six digits, with and without "#"
    ("#ff8800", (255, 136, 0)),
    ("ff8800", (255, 136, 0)),
    ("#123456", (18, 52, 86)),
    ("#000000", (0, 0, 0)),
    ("#ffffff", (255, 255, 255)),
    # Three digits: every digit is doubled
    ("#f80", (255, 136, 0)),
    ("f80", (255, 136, 0)),
    ("#123", (17, 34, 51)),
    ("#abc", (170, 187, 204)),
    ("#000", (0, 0, 0)),
    ("#fff", (255, 255, 255)),
    # Upper and mixed case
    ("#FF8800", (255, 136, 0)),
    ("#aBc123", (171, 193, 35)),
    ("#F80", (255, 136, 0)),
]

NOT_A_COLOR = [
    # Text of the wrong shape
    "",
    "#",
    "f",
    "ff",
    "#ffff",
    "#fffff",
    "#fffffff",
    "#ff8800ff",
    "#gg8800",
    "#ff88zz",
    " ff8800",
    "ff8800 ",
    "ff8800\n",
    "ff 8800",
    "##ff8800",
    "0xff8800",
    "orange",
    "ＦＦ８８００",
    # Not text at all
    None,
    0xFF8800,
    255,
    1.5,
    True,
    b"ff8800",
    ["f", "f", "8"],
    (255, 136, 0),
    {"r": 255},
    object(),
]


@pytest.mark.parametrize("text, channels", PARSED)
def test_reads_the_three_channels(text: str, channels: tuple[int, int, int]) -> None:
    assert parse_hex_color(text) == channels


@pytest.mark.parametrize("text, channels", PARSED)
def test_the_result_is_a_tuple_of_three_ints(text: str, channels: tuple[int, int, int]) -> None:
    result = parse_hex_color(text)

    assert type(result) is tuple
    assert len(result) == 3
    assert all(type(channel) is int for channel in result)
    assert all(0 <= channel <= 255 for channel in result)


@pytest.mark.parametrize("value", NOT_A_COLOR)
def test_gives_none_for_everything_else_and_never_raises(value: object) -> None:
    assert parse_hex_color(value) is None


def test_the_short_form_means_the_same_as_the_long_form() -> None:
    assert parse_hex_color("#f80") == parse_hex_color("#ff8800")
    assert parse_hex_color("#abc") == parse_hex_color("#aabbcc")


def test_the_hash_makes_no_difference() -> None:
    assert parse_hex_color("#ff8800") == parse_hex_color("ff8800")
    assert parse_hex_color("#f80") == parse_hex_color("f80")


def test_the_letter_case_makes_no_difference() -> None:
    assert parse_hex_color("#ABCDEF") == parse_hex_color("#abcdef")
