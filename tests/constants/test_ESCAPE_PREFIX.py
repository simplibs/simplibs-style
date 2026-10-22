# Outers
from simplibs.style.constants import ESCAPE_PREFIX


def test_is_the_escape_character_and_a_bracket() -> None:
    assert ESCAPE_PREFIX == "\033["
    assert ESCAPE_PREFIX == "\x1b["


def test_is_a_two_character_string() -> None:
    assert isinstance(ESCAPE_PREFIX, str)
    assert len(ESCAPE_PREFIX) == 2


def test_starts_with_the_escape_character() -> None:
    assert ord(ESCAPE_PREFIX[0]) == 27
    assert ESCAPE_PREFIX[1] == "["
