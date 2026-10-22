import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.base_class import StyleDefiner
from simplibs.style.colors import color_hex, color_rgb


RESET = "\033[0m"

# (text, the same color as RGB)
SPELLINGS = [
    ("#ff8800", (255, 136, 0)),
    ("ff8800", (255, 136, 0)),
    ("#f80", (255, 136, 0)),
    ("f80", (255, 136, 0)),
    ("#FF8800", (255, 136, 0)),
    ("#F80", (255, 136, 0)),
    ("#000", (0, 0, 0)),
    ("#ffffff", (255, 255, 255)),
    ("#123456", (18, 52, 86)),
    ("#abc", (170, 187, 204)),
]


@pytest.mark.parametrize("text, rgb", SPELLINGS)
def test_equals_the_rgb_style_of_the_same_color(text: str, rgb: tuple[int, int, int]) -> None:
    assert color_hex(text) == color_rgb(*rgb)


@pytest.mark.parametrize("text, rgb", SPELLINGS)
def test_equals_the_rgb_style_of_the_same_color_as_background(text: str, rgb: tuple[int, int, int]) -> None:
    assert color_hex(text, background=True) == color_rgb(*rgb, background=True)


def test_a_text_color_is_38_2_r_g_b() -> None:
    style = color_hex("#ff8800")

    assert style.codes == ("38;2;255;136;0",)
    assert style.sequence == "\033[38;2;255;136;0m"


def test_a_background_color_is_48_2_r_g_b() -> None:
    style = color_hex("#ff8800", background=True)

    assert style.codes == ("48;2;255;136;0",)
    assert style.sequence == "\033[48;2;255;136;0m"


def test_background_false_is_the_same_as_the_default() -> None:
    assert color_hex("#ff8800", background=False) == color_hex("#ff8800")


def test_every_spelling_of_one_color_gives_one_style() -> None:
    styles = {color_hex(text) for text in ("#ff8800", "ff8800", "#f80", "f80", "#FF8800")}

    assert len(styles) == 1


def test_returns_a_style_definer() -> None:
    assert isinstance(color_hex("#ff8800"), StyleDefiner)


def test_styles_a_text() -> None:
    assert color_hex("#ff8800")("x", use_style=True) == f"\033[38;2;255;136;0mx{RESET}"


def test_combines_with_other_styles() -> None:
    combined = color_hex("#ff8800") + StyleDefiner("1")

    assert combined.codes == ("38;2;255;136;0", "1")


def test_background_can_only_be_given_by_name() -> None:
    with pytest.raises(TypeError):
        color_hex("#ff8800", True)  # type: ignore[misc]


# ----------------------------------------------------------------------
# What is refused
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "value",
    [
        "",
        "#",
        "f",
        "#ff",
        "#ffff",
        "#fffff",
        "#fffffff",
        "#ff8800ff",
        "#gg8800",
        " ff8800",
        "ff8800 ",
        "ff8800\n",
        "##ff8800",
        "0xff8800",
        "orange",
    ],
)
def test_a_text_that_is_not_a_hex_color_is_refused_as_a_value_error(value: str) -> None:
    with pytest.raises(ParamError) as caught:
        color_hex(value)

    assert caught.value.error_name == "STYLE_COLOR_HEX_INVALID"
    assert caught.value.label == "hex color"
    assert isinstance(caught.value, ValueError)


@pytest.mark.parametrize("value", [None, 0xFF8800, 255, 1.5, True, b"ff8800", ["f", "f", "8"], (255, 136, 0)])
def test_a_value_that_is_not_text_is_refused_as_a_type_error(value: object) -> None:
    with pytest.raises(ParamError) as caught:
        color_hex(value)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_HEX_INVALID"
    assert isinstance(caught.value, TypeError)


@pytest.mark.parametrize("background", [1, 0, "yes", "", None, [], 1.0])
def test_a_background_that_is_not_a_bool_is_refused(background: object) -> None:
    with pytest.raises(ParamError) as caught:
        color_hex("#ff8800", background=background)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_BACKGROUND_NOT_BOOL"
