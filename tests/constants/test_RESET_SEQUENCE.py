# Outers
from simplibs.style.constants import RESET_SEQUENCE


def test_is_the_complete_reset() -> None:
    assert RESET_SEQUENCE == "\033[0m"
    assert RESET_SEQUENCE == "\x1b[0m"


def test_is_a_four_character_string() -> None:
    assert isinstance(RESET_SEQUENCE, str)
    assert len(RESET_SEQUENCE) == 4


def test_is_framed_like_every_sequence() -> None:
    assert RESET_SEQUENCE.startswith("\033[")
    assert RESET_SEQUENCE.endswith("m")
