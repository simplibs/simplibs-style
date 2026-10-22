import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.colors._helpers import choose_color_introducer


def test_a_text_color_is_introduced_by_38() -> None:
    assert choose_color_introducer(False) == "38"


def test_a_background_color_is_introduced_by_48() -> None:
    assert choose_color_introducer(True) == "48"


@pytest.mark.parametrize("background", [True, False])
def test_the_answer_is_a_string(background: bool) -> None:
    assert type(choose_color_introducer(background)) is str


@pytest.mark.parametrize("background", [1, 0, 1.0, "True", "", None, [], object()])
def test_refuses_everything_that_is_not_a_bool(background: object) -> None:
    with pytest.raises(ParamError) as caught:
        choose_color_introducer(background)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_COLOR_BACKGROUND_NOT_BOOL"
    assert isinstance(caught.value, TypeError)
