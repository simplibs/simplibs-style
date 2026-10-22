# Outers
from simplibs.style.constants import ESCAPE_SUFFIX


def test_is_the_letter_m() -> None:
    assert ESCAPE_SUFFIX == "m"


def test_is_a_string() -> None:
    assert isinstance(ESCAPE_SUFFIX, str)
