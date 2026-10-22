import io
import sys

import pytest
# Outers
from simplibs.style.settings._helpers._is_stdout_terminal import _is_stdout_terminal


class StreamWithIsatty:
    """A stream whose `isatty()` answers with the given value."""

    def __init__(self, answer: object) -> None:
        self._answer = answer

    def isatty(self) -> object:
        return self._answer


class StreamWithBrokenIsatty:
    """A stream whose `isatty()` raises the given exception."""

    def __init__(self, error: Exception) -> None:
        self._error = error

    def isatty(self) -> bool:
        raise self._error


def test_a_terminal_is_a_terminal(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", StreamWithIsatty(True))

    assert _is_stdout_terminal() is True


def test_a_pipe_or_file_is_not_a_terminal(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", StreamWithIsatty(False))

    assert _is_stdout_terminal() is False


def test_a_captured_stream_is_not_a_terminal(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", io.StringIO())

    assert _is_stdout_terminal() is False


def test_a_missing_stream_is_not_a_terminal(monkeypatch) -> None:
    # Windowed applications have no stdout at all
    monkeypatch.setattr(sys, "stdout", None)

    assert _is_stdout_terminal() is False


def test_a_closed_stream_is_not_a_terminal(monkeypatch) -> None:
    stream = io.StringIO()
    stream.close()
    monkeypatch.setattr(sys, "stdout", stream)

    assert _is_stdout_terminal() is False


def test_an_object_without_isatty_is_not_a_terminal(monkeypatch) -> None:
    monkeypatch.setattr(sys, "stdout", object())

    assert _is_stdout_terminal() is False


@pytest.mark.parametrize("error", [ValueError("closed"), OSError("broken"), AttributeError("odd")])
def test_a_stream_that_fails_when_asked_is_not_a_terminal(monkeypatch, error: Exception) -> None:
    monkeypatch.setattr(sys, "stdout", StreamWithBrokenIsatty(error))

    assert _is_stdout_terminal() is False


@pytest.mark.parametrize("answer, expected", [(1, True), (0, False), ("yes", True), ("", False)])
def test_the_answer_is_always_a_bool(monkeypatch, answer: object, expected: bool) -> None:
    monkeypatch.setattr(sys, "stdout", StreamWithIsatty(answer))

    assert _is_stdout_terminal() is expected
