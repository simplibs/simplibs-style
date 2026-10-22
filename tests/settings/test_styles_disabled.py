import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.settings import get_styles_enabled, styles_disabled, styles_enabled
from simplibs.style.settings._classes import StylesOverride
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


def test_returns_a_styles_override_that_says_false() -> None:
    manager = styles_disabled()

    assert isinstance(manager, StylesOverride)
    assert repr(manager) == "StylesOverride(False)"


def test_every_call_gives_a_new_manager() -> None:
    assert styles_disabled() is not styles_disabled()


@pytest.mark.parametrize("global_value", [True, False])
def test_styles_are_off_inside_the_block_and_back_afterwards(global_value: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = global_value

    with styles_disabled():
        assert get_styles_enabled() is False

    assert get_styles_enabled() is global_value


def test_the_state_comes_back_after_an_exception() -> None:
    GLOBAL_STYLES_SWITCH.enabled = True

    with pytest.raises(RuntimeError):
        with styles_disabled():
            raise RuntimeError("boom")

    assert get_styles_enabled() is True


def test_works_as_a_decorator() -> None:
    GLOBAL_STYLES_SWITCH.enabled = True

    @styles_disabled()
    def render() -> bool:
        return get_styles_enabled()

    assert render() is False
    assert get_styles_enabled() is True


def test_the_innermost_block_decides() -> None:
    GLOBAL_STYLES_SWITCH.enabled = True

    with styles_disabled():
        with styles_enabled():
            assert get_styles_enabled() is True
        assert get_styles_enabled() is False

    assert get_styles_enabled() is True


def test_nested_disabled_blocks_stay_disabled() -> None:
    GLOBAL_STYLES_SWITCH.enabled = True

    with styles_disabled():
        with styles_disabled():
            assert get_styles_enabled() is False
        assert get_styles_enabled() is False


def test_cannot_be_used_as_a_yes_no_value() -> None:
    with pytest.raises(ParamError):
        bool(styles_disabled())
