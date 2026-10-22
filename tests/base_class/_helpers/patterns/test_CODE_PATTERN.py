import re

import pytest
# Outers
from simplibs.style.base_class._helpers.patterns import CODE_PATTERN


VALID = [
    "0",
    "1",
    "91",
    "007",
    "999",
    "38;5;208",
    "38;2;255;136;0",
    "1;31",
]

INVALID = [
    # Nothing, or only separators
    "",
    ";",
    ";;",
    # Misplaced or doubled separators
    "1;",
    ";1",
    "1;;2",
    # Not digits
    "9x",
    "m",
    "91m",
    "-1",
    "1.5",
    "1,2",
    "1:2",
    # Surrounding text
    " 1",
    "1 ",
    "1\n",
    "\n1",
    "\033[91m",
    # Digits that are not ASCII digits
    "²",
    "٣",
    "１",
]


def test_is_a_compiled_pattern() -> None:
    assert isinstance(CODE_PATTERN, re.Pattern)


@pytest.mark.parametrize("code", VALID)
def test_accepts_a_bare_code(code: str) -> None:
    match = CODE_PATTERN.fullmatch(code)

    assert match is not None
    assert match.group(0) == code


@pytest.mark.parametrize("code", INVALID)
def test_refuses_everything_else(code: str) -> None:
    assert CODE_PATTERN.fullmatch(code) is None
