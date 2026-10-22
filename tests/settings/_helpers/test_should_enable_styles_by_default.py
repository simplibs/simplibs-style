import sys

import pytest
# Outers
from simplibs.style.settings._helpers import should_enable_styles_by_default


class FakeStream:
    """A stream that is, or is not, a terminal."""

    def __init__(self, is_terminal: bool) -> None:
        self._is_terminal = is_terminal

    def isatty(self) -> bool:
        return self._is_terminal


# (environment, standard output is a terminal, styles are on)
CASES = [
    # Nothing is said: only the terminal decides
    pytest.param({}, True, True, id="nothing-set-terminal"),
    pytest.param({}, False, False, id="nothing-set-pipe"),
    # TERM=dumb
    pytest.param({"TERM": "dumb"}, True, False, id="dumb-terminal"),
    pytest.param({"TERM": "xterm-256color"}, True, True, id="normal-term-terminal"),
    pytest.param({"TERM": "xterm-256color"}, False, False, id="normal-term-pipe"),
    # NO_COLOR is a refusal that beats everything
    pytest.param({"NO_COLOR": "1"}, True, False, id="no-color-terminal"),
    pytest.param({"NO_COLOR": "0"}, True, False, id="no-color-zero-still-counts"),
    pytest.param({"NO_COLOR": "1", "FORCE_COLOR": "1"}, True, False, id="no-color-beats-force-color"),
    pytest.param({"NO_COLOR": "1", "FORCE_COLOR": "1"}, False, False, id="no-color-beats-force-color-pipe"),
    # FORCE_COLOR is a request that beats the terminal and TERM
    pytest.param({"FORCE_COLOR": "1"}, False, True, id="force-color-pipe"),
    pytest.param({"FORCE_COLOR": "1"}, True, True, id="force-color-terminal"),
    pytest.param({"FORCE_COLOR": "1", "TERM": "dumb"}, False, True, id="force-color-beats-dumb"),
    # An empty value is the same as no value
    pytest.param({"NO_COLOR": ""}, True, True, id="empty-no-color-ignored"),
    pytest.param({"NO_COLOR": "  "}, True, True, id="blank-no-color-ignored"),
    pytest.param({"NO_COLOR": "", "FORCE_COLOR": "1"}, False, True, id="empty-no-color-does-not-block-force"),
    pytest.param({"FORCE_COLOR": ""}, False, False, id="empty-force-color-ignored"),
]


@pytest.mark.parametrize("environment, is_terminal, expected", CASES)
def test_decision(
    monkeypatch,
    clean_environment,
    environment: dict[str, str],
    is_terminal: bool,
    expected: bool,
) -> None:
    for name, value in environment.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(sys, "stdout", FakeStream(is_terminal))

    assert should_enable_styles_by_default() is expected


def test_reads_the_environment_on_every_call(monkeypatch, clean_environment) -> None:
    monkeypatch.setattr(sys, "stdout", FakeStream(True))
    assert should_enable_styles_by_default() is True

    monkeypatch.setenv("NO_COLOR", "1")
    assert should_enable_styles_by_default() is False

    monkeypatch.delenv("NO_COLOR")
    assert should_enable_styles_by_default() is True
