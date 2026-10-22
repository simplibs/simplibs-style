import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.base_class import StyleDefiner
from simplibs.style.colors import color_256


RESET = "\033[0m"


@pytest.mark.parametrize("n", [0, 7, 8, 15, 16, 208, 231, 232, 255])
def test_a_text_color_is_38_5_n(n: int) -> None:
    style = color_256(n)

    assert style.codes == (f"38;5;{n}",)
    assert style.sequence == f"\033[38;5;{n}m"


@pytest.mark.parametrize("n", [0, 7, 8, 15, 16, 208, 231, 232, 255])
def test_a_background_color_is_48_5_n(n: int) -> None:
    style = color_256(n, background=True)

    assert style.codes == (f"48;5;{n}",)
    assert style.sequence == f"\033[48;5;{n}m"


def test_background_false_is_the_same_as_the_default() -> None:
    assert color_256(208, background=False) == color_256(208)


def test_returns_a_style_definer() -> None:
    assert isinstance(color_256(208), StyleDefiner)


def test_equals_the_same_style_written_by_hand() -> None:
    assert color_256(208) == StyleDefiner("38;5;208")
    assert color_256(208, background=True) == StyleDefiner("48;5;208")


def test_text_and_background_differ() -> None:
    assert color_256(208) != color_256(208, background=True)


def test_different_indexes_differ() -> None:
    assert color_256(1) != color_256(2)


def test_styles_a_text() -> None:
    assert color_256(208)("x", use_style=True) == f"\033[38;5;208mx{RESET}"
    assert color_256(208, background=True)("x", use_style=True) == f"\033[48;5;208mx{RESET}"


def test_combines_with_other_styles() -> None:
    combined = color_256(208) + StyleDefiner("1")

    assert combined.codes == ("38;5;208", "1")
    assert combined.sequence == "\033[38;5;208;1m"


def test_background_can_only_be_given_by_name() -> None:
    with pytest.raises(TypeError):
        color_256(208, True)  # type: ignore[misc]


@pytest.mark.parametrize("n", [-1, 256, 300, 1000, -255])
def test_an_index_outside_the_palette_is_refused(n: int) -> None:
    with pytest.raises(ParamError) as caught:
        color_256(n)

    assert caught.value.error_name == "STYLE_COLOR_OUT_OF_RANGE"
    assert caught.value.label == "n"
    assert isinstance(caught.value, ValueError)


@pytest.mark.parametrize("n", ["208", 208.0, 1.5, None, True, False, [208], (208,)])
def test_an_index_that_is_not_an_integer_is_refused(n: object) -> None:
    with pytest.raises(ParamError) as caught:
        color_256(n)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_NOT_INT"
    assert caught.value.label == "n"
    assert isinstance(caught.value, TypeError)


@pytest.mark.parametrize("background", [1, 0, "yes", "", None, [], 1.0])
def test_a_background_that_is_not_a_bool_is_refused(background: object) -> None:
    with pytest.raises(ParamError) as caught:
        color_256(208, background=background)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_BACKGROUND_NOT_BOOL"
    assert isinstance(caught.value, TypeError)
