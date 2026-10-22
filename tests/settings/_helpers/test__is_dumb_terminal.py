import pytest
# Outers
from simplibs.style.settings._helpers._is_dumb_terminal import _is_dumb_terminal


@pytest.mark.parametrize("term", ["dumb", "DUMB", "Dumb", " dumb ", "dumb\n"])
def test_dumb_in_any_spelling_is_a_dumb_terminal(monkeypatch, term: str) -> None:
    monkeypatch.setenv("TERM", term)

    assert _is_dumb_terminal() is True


@pytest.mark.parametrize("term", ["xterm", "xterm-256color", "screen", "linux", "vt100", "dumber", "not-dumb", ""])
def test_any_other_value_is_not_a_dumb_terminal(monkeypatch, term: str) -> None:
    monkeypatch.setenv("TERM", term)

    assert _is_dumb_terminal() is False


def test_a_missing_term_is_unknown_not_dumb(monkeypatch) -> None:
    monkeypatch.delenv("TERM", raising=False)

    assert _is_dumb_terminal() is False
