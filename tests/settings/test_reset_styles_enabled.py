import sys

import pytest
# Outers
from simplibs.style.settings import get_styles_enabled, reset_styles_enabled, set_styles_enabled
from simplibs.style.settings._classes import StylesOverride
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


class FakeStream:
    """A stream that is, or is not, a terminal."""

    def __init__(self, is_terminal: bool) -> None:
        self._is_terminal = is_terminal

    def isatty(self) -> bool:
        return self._is_terminal


@pytest.fixture(autouse=True)
def quiet_environment(clean_environment) -> None:
    """Every test here starts from an environment that says nothing."""


def test_returns_nothing(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))

    assert reset_styles_enabled() is None


@pytest.mark.parametrize("is_terminal", [True, False])
@pytest.mark.parametrize("moved_to", [True, False])
def test_brings_back_what_the_environment_says(monkeypatch, is_terminal: bool, moved_to: bool) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(is_terminal))
    set_styles_enabled(moved_to)

    reset_styles_enabled()

    assert get_styles_enabled() is is_terminal


def test_no_color_turns_styles_off(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))
    monkeypatch.setenv("NO_COLOR", "1")
    set_styles_enabled(True)

    reset_styles_enabled()

    assert GLOBAL_STYLES_SWITCH.enabled is False


def test_force_color_turns_styles_on_even_without_a_terminal(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(False))
    monkeypatch.setenv("FORCE_COLOR", "1")
    set_styles_enabled(False)

    reset_styles_enabled()

    assert GLOBAL_STYLES_SWITCH.enabled is True


def test_reads_the_environment_again_on_every_call(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))

    reset_styles_enabled()
    assert GLOBAL_STYLES_SWITCH.enabled is True

    monkeypatch.setenv("NO_COLOR", "1")
    reset_styles_enabled()
    assert GLOBAL_STYLES_SWITCH.enabled is False

    monkeypatch.delenv("NO_COLOR")
    reset_styles_enabled()
    assert GLOBAL_STYLES_SWITCH.enabled is True


def test_the_stored_answer_is_a_bool(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))
    monkeypatch.setenv("FORCE_COLOR", "1")

    reset_styles_enabled()

    assert type(GLOBAL_STYLES_SWITCH.enabled) is bool


def test_a_scoped_override_still_wins_but_the_switch_has_moved(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))
    set_styles_enabled(False)

    with StylesOverride(False):
        reset_styles_enabled()

        assert get_styles_enabled() is False
        assert GLOBAL_STYLES_SWITCH.enabled is True

    assert get_styles_enabled() is True
