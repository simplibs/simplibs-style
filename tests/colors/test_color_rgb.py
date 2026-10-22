import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.base_class import StyleDefiner
from simplibs.style.colors import color_rgb


RESET = "\033[0m"

COLORS = [
    (0, 0, 0),
    (255, 255, 255),
    (255, 136, 0),
    (1, 2, 3),
    (0, 255, 0),
    (18, 52, 86),
]


@pytest.mark.parametrize("r, g, b", COLORS)
def test_a_text_color_is_38_2_r_g_b(r: int, g: int, b: int) -> None:
    style = color_rgb(r, g, b)

    assert style.codes == (f"38;2;{r};{g};{b}",)
    assert style.sequence == f"\033[38;2;{r};{g};{b}m"


@pytest.mark.parametrize("r, g, b", COLORS)
def test_a_background_color_is_48_2_r_g_b(r: int, g: int, b: int) -> None:
    style = color_rgb(r, g, b, background=True)

    assert style.codes == (f"48;2;{r};{g};{b}",)
    assert style.sequence == f"\033[48;2;{r};{g};{b}m"


def test_the_channels_keep_their_order() -> None:
    assert color_rgb(1, 2, 3).codes == ("38;2;1;2;3",)
    assert color_rgb(3, 2, 1).codes == ("38;2;3;2;1",)


def test_background_false_is_the_same_as_the_default() -> None:
    assert color_rgb(255, 136, 0, background=False) == color_rgb(255, 136, 0)


def test_returns_a_style_definer() -> None:
    assert isinstance(color_rgb(255, 136, 0), StyleDefiner)


def test_equals_the_same_style_written_by_hand() -> None:
    assert color_rgb(255, 136, 0) == StyleDefiner("38;2;255;136;0")
    assert color_rgb(255, 136, 0, background=True) == StyleDefiner("48;2;255;136;0")


def test_text_and_background_differ() -> None:
    assert color_rgb(255, 136, 0) != color_rgb(255, 136, 0, background=True)


def test_styles_a_text() -> None:
    assert color_rgb(255, 136, 0)("x", use_style=True) == f"\033[38;2;255;136;0mx{RESET}"
    assert color_rgb(255, 136, 0, background=True)("x", use_style=True) == f"\033[48;2;255;136;0mx{RESET}"


def test_combines_with_other_styles() -> None:
    combined = color_rgb(255, 136, 0) + StyleDefiner("1")

    assert combined.codes == ("38;2;255;136;0", "1")


def test_background_can_only_be_given_by_name() -> None:
    with pytest.raises(TypeError):
        color_rgb(1, 2, 3, True)  # type: ignore[misc]


# ----------------------------------------------------------------------
# Every channel is checked and named in the error
# ----------------------------------------------------------------------
@pytest.mark.parametrize("position, label", [(0, "r"), (1, "g"), (2, "b")])
@pytest.mark.parametrize("bad", [-1, 256, 1000])
def test_a_channel_outside_one_byte_is_refused_by_name(position: int, label: str, bad: int) -> None:
    channels = [10, 20, 30]
    channels[position] = bad

    with pytest.raises(ParamError) as caught:
        color_rgb(*channels)

    assert caught.value.error_name == "STYLE_COLOR_OUT_OF_RANGE"
    assert caught.value.label == label
    assert isinstance(caught.value, ValueError)


@pytest.mark.parametrize("position, label", [(0, "r"), (1, "g"), (2, "b")])
@pytest.mark.parametrize("bad", ["10", 10.0, None, True, [10]])
def test_a_channel_that_is_not_an_integer_is_refused_by_name(position: int, label: str, bad: object) -> None:
    channels: list[object] = [10, 20, 30]
    channels[position] = bad

    with pytest.raises(ParamError) as caught:
        color_rgb(*channels)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_NOT_INT"
    assert caught.value.label == label
    assert isinstance(caught.value, TypeError)


def test_the_first_bad_channel_is_the_one_reported() -> None:
    with pytest.raises(ParamError) as caught:
        color_rgb(300, "x", None)  # type: ignore[arg-type]

    assert caught.value.label == "r"


@pytest.mark.parametrize("background", [1, 0, "yes", "", None, [], 1.0])
def test_a_background_that_is_not_a_bool_is_refused(background: object) -> None:
    with pytest.raises(ParamError) as caught:
        color_rgb(255, 136, 0, background=background)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_BACKGROUND_NOT_BOOL"
    assert isinstance(caught.value, TypeError)
