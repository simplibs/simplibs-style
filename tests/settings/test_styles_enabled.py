import sys

import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.settings import get_styles_enabled, reset_styles_enabled, styles_disabled, styles_enabled
from simplibs.style.settings._classes import StylesOverride
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


class FakeStream:
    """A stream that is not a terminal."""

    def isatty(self) -> bool:
        return False


def test_returns_a_styles_override_that_says_true() -> None:
    manager = styles_enabled()

    assert isinstance(manager, StylesOverride)
    assert repr(manager) == "StylesOverride(True)"


def test_every_call_gives_a_new_manager() -> None:
    assert styles_enabled() is not styles_enabled()


@pytest.mark.parametrize("global_value", [True, False])
def test_styles_are_on_inside_the_block_and_back_afterwards(global_value: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = global_value

    with styles_enabled():
        assert get_styles_enabled() is True

    assert get_styles_enabled() is global_value


def test_forces_styles_on_when_the_environment_asks_for_none(monkeypatch, clean_environment) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream())
    monkeypatch.setenv("NO_COLOR", "1")
    reset_styles_enabled()
    assert get_styles_enabled() is False

    with styles_enabled():
        assert get_styles_enabled() is True

    assert get_styles_enabled() is False


def test_the_state_comes_back_after_an_exception() -> None:
    GLOBAL_STYLES_SWITCH.enabled = False

    with pytest.raises(RuntimeError):
        with styles_enabled():
            raise RuntimeError("boom")

    assert get_styles_enabled() is False


def test_works_as_a_decorator() -> None:
    GLOBAL_STYLES_SWITCH.enabled = False

    @styles_enabled()
    def render() -> bool:
        return get_styles_enabled()

    assert render() is True
    assert get_styles_enabled() is False


def test_the_innermost_block_decides() -> None:
    GLOBAL_STYLES_SWITCH.enabled = False

    with styles_enabled():
        with styles_disabled():
            assert get_styles_enabled() is False
        assert get_styles_enabled() is True

    assert get_styles_enabled() is False


def test_cannot_be_used_as_a_yes_no_value() -> None:
    with pytest.raises(ParamError):
        bool(styles_enabled())
