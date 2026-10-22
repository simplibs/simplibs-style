import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.settings import get_styles_enabled, set_styles_enabled
from simplibs.style.settings._classes import StylesOverride
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


@pytest.mark.parametrize("value", [True, False])
def test_moves_the_process_wide_switch(value: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = not value

    set_styles_enabled(value)

    assert GLOBAL_STYLES_SWITCH.enabled is value
    assert get_styles_enabled() is value


def test_returns_nothing() -> None:
    assert set_styles_enabled(True) is None


def test_can_be_repeated_and_reversed() -> None:
    set_styles_enabled(True)
    set_styles_enabled(True)
    assert get_styles_enabled() is True

    set_styles_enabled(False)
    assert get_styles_enabled() is False


@pytest.mark.parametrize("value", [1, 0, 1.0, "True", "", None, [], (True,), object()])
def test_refuses_everything_that_is_not_a_bool(value: object) -> None:
    with pytest.raises(ParamError) as caught:
        set_styles_enabled(value)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_STYLES_ENABLED_NOT_BOOL"


def test_the_refusal_is_also_a_type_error() -> None:
    with pytest.raises(TypeError):
        set_styles_enabled("yes")  # type: ignore[arg-type]


@pytest.mark.parametrize("start", [True, False])
def test_a_refused_value_leaves_the_switch_where_it_was(start: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = start

    with pytest.raises(ParamError):
        set_styles_enabled(1)  # type: ignore[arg-type]

    assert GLOBAL_STYLES_SWITCH.enabled is start


def test_a_scoped_override_still_wins_but_the_switch_has_moved() -> None:
    GLOBAL_STYLES_SWITCH.enabled = False

    with StylesOverride(False):
        set_styles_enabled(True)

        assert get_styles_enabled() is False
        assert GLOBAL_STYLES_SWITCH.enabled is True

    assert get_styles_enabled() is True
