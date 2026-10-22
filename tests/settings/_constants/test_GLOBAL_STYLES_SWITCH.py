import importlib.util
import sys
from types import ModuleType

import pytest
# Outers
from simplibs.style.settings._classes import StylesSwitch
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


MODULE_NAME = "simplibs.style.settings._constants.GLOBAL_STYLES_SWITCH"


class FakeStream:
    """A stream that is, or is not, a terminal."""

    def __init__(self, is_terminal: bool) -> None:
        self._is_terminal = is_terminal

    def isatty(self) -> bool:
        return self._is_terminal


def run_module_again() -> ModuleType:
    """Execute the module once more, as a first import would, without registering it.

    The real switch that the whole library shares stays untouched.
    """

    spec = importlib.util.find_spec(MODULE_NAME)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ----------------------------------------------------------------------
# The shared switch
# ----------------------------------------------------------------------
def test_is_a_styles_switch() -> None:
    assert isinstance(GLOBAL_STYLES_SWITCH, StylesSwitch)


def test_holds_a_bool() -> None:
    assert isinstance(GLOBAL_STYLES_SWITCH.enabled, bool)


def test_can_be_moved_in_both_directions() -> None:
    GLOBAL_STYLES_SWITCH.enabled = True
    assert GLOBAL_STYLES_SWITCH.enabled is True

    GLOBAL_STYLES_SWITCH.enabled = False
    assert GLOBAL_STYLES_SWITCH.enabled is False


# ----------------------------------------------------------------------
# Its starting position comes from the environment at import
# ----------------------------------------------------------------------
def test_starts_on_in_a_terminal(monkeypatch, clean_environment) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))

    assert run_module_again().GLOBAL_STYLES_SWITCH.enabled is True


def test_starts_off_in_a_pipe(monkeypatch, clean_environment) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(False))

    assert run_module_again().GLOBAL_STYLES_SWITCH.enabled is False


def test_starts_off_when_no_color_is_set(monkeypatch, clean_environment) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))
    monkeypatch.setenv("NO_COLOR", "1")

    assert run_module_again().GLOBAL_STYLES_SWITCH.enabled is False


def test_starts_on_when_force_color_is_set(monkeypatch, clean_environment) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(False))
    monkeypatch.setenv("FORCE_COLOR", "1")

    assert run_module_again().GLOBAL_STYLES_SWITCH.enabled is True


def test_running_the_module_again_does_not_touch_the_shared_switch(monkeypatch, clean_environment) -> None:
    GLOBAL_STYLES_SWITCH.enabled = False
    monkeypatch.setattr(sys, "stdout", FakeStream(True))

    fresh = run_module_again().GLOBAL_STYLES_SWITCH

    assert fresh is not GLOBAL_STYLES_SWITCH
    assert GLOBAL_STYLES_SWITCH.enabled is False
