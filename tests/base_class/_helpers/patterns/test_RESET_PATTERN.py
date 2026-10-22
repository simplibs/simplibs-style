import re

import pytest
# Outers
from simplibs.style.base_class._helpers.patterns import RESET_PATTERN


LONE_RESETS = [
    "\033[0m",
    "\033[00m",
    "\033[000m",
    "\033[m",
]

NOT_LONE_RESETS = [
    # A reset combined with other codes
    "\033[0;1m",
    "\033[1;0m",
    # Other sequences
    "\033[1m",
    "\033[01m",
    "\033[10m",
    "\033[30m",
    "\033[39m",
    "\033[91m",
    # Pieces of a reset
    "\033[0",
    "[0m",
    "0m",
    "m",
    "",
]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(RESET_PATTERN, re.Pattern)


@pytest.mark.parametrize("sequence", LONE_RESETS)
def test_recognizes_every_spelling_of_the_lone_reset(sequence: str) -> None:
    assert RESET_PATTERN.fullmatch(sequence) is not None


@pytest.mark.parametrize("sequence", NOT_LONE_RESETS)
def test_leaves_everything_else_alone(sequence: str) -> None:
    assert RESET_PATTERN.fullmatch(sequence) is None


def test_finds_every_reset_inside_a_text() -> None:
    text = "a\033[0mb\033[mc\033[00md"

    assert len(RESET_PATTERN.findall(text)) == 3


def test_does_not_find_a_reset_inside_a_longer_sequence() -> None:
    assert RESET_PATTERN.search("x\033[0;1my") is None
    assert RESET_PATTERN.search("x\033[10my") is None
    assert RESET_PATTERN.search("x\033[30my") is None


def test_finds_only_the_reset_next_to_another_sequence() -> None:
    text = "\033[1mbold\033[0m"

    assert [match.group(0) for match in RESET_PATTERN.finditer(text)] == ["\033[0m"]
