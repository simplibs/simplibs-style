import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.base_class._helpers import normalize_code


# (input, the bare code)
ACCEPTED = [
    # The bare form
    ("91", "91"),
    ("0", "0"),
    ("007", "007"),
    ("38;5;208", "38;5;208"),
    ("38;2;255;136;0", "38;2;255;136;0"),
    ("1;31", "1;31"),
    # With the trailing "m"
    ("91m", "91"),
    ("0m", "0"),
    ("38;5;208m", "38;5;208"),
    # The full escape sequence
    ("\033[91m", "91"),
    ("\033[0m", "0"),
    ("\033[38;5;208m", "38;5;208"),
    ("\033[38;2;255;136;0m", "38;2;255;136;0"),
    ("\x1b[1;31m", "1;31"),
]

# (input, error name, the built-in error the ParamError also is)
REFUSED = [
    # Not text
    (91, "STYLE_CODE_NOT_TEXT", TypeError),
    (None, "STYLE_CODE_NOT_TEXT", TypeError),
    (b"91", "STYLE_CODE_NOT_TEXT", TypeError),
    (["91"], "STYLE_CODE_NOT_TEXT", TypeError),
    (True, "STYLE_CODE_NOT_TEXT", TypeError),
    (9.1, "STYLE_CODE_NOT_TEXT", TypeError),
    # Nothing is left once the frame is taken off
    ("", "STYLE_EMPTY_CODE", ValueError),
    ("   ", "STYLE_EMPTY_CODE", ValueError),
    ("m", "STYLE_EMPTY_CODE", ValueError),
    ("\033[m", "STYLE_EMPTY_CODE", ValueError),
    ("\033[ m", "STYLE_EMPTY_CODE", ValueError),
    # An escape sequence that does not end with "m"
    ("\033[", "STYLE_INVALID_ANSI_FORMAT", ValueError),
    ("\033[91", "STYLE_INVALID_ANSI_FORMAT", ValueError),
    ("\033[91x", "STYLE_INVALID_ANSI_FORMAT", ValueError),
    ("\033[91 ", "STYLE_INVALID_ANSI_FORMAT", ValueError),
    # A body that is not digits joined by semicolons
    ("abc", "STYLE_INVALID_CODE", ValueError),
    ("9x", "STYLE_INVALID_CODE", ValueError),
    ("1;", "STYLE_INVALID_CODE", ValueError),
    (";1", "STYLE_INVALID_CODE", ValueError),
    (";;", "STYLE_INVALID_CODE", ValueError),
    ("1;;2", "STYLE_INVALID_CODE", ValueError),
    (" 91", "STYLE_INVALID_CODE", ValueError),
    ("91 ", "STYLE_INVALID_CODE", ValueError),
    ("9 1", "STYLE_INVALID_CODE", ValueError),
    ("-1", "STYLE_INVALID_CODE", ValueError),
    ("1.5", "STYLE_INVALID_CODE", ValueError),
    ("٣", "STYLE_INVALID_CODE", ValueError),
    ("mm", "STYLE_INVALID_CODE", ValueError),
    ("91mm", "STYLE_INVALID_CODE", ValueError),
    ("m91", "STYLE_INVALID_CODE", ValueError),
    ("\033[;m", "STYLE_INVALID_CODE", ValueError),
    ("\033[91mm", "STYLE_INVALID_CODE", ValueError),
]


@pytest.mark.parametrize("code, expected", ACCEPTED)
def test_reduces_every_spelling_to_the_bare_code(code: str, expected: str) -> None:
    assert normalize_code(code) == expected


@pytest.mark.parametrize("code, expected", ACCEPTED)
def test_the_result_is_a_plain_string(code: str, expected: str) -> None:
    assert type(normalize_code(code)) is str


@pytest.mark.parametrize("code, expected", ACCEPTED)
def test_normalizing_twice_changes_nothing(code: str, expected: str) -> None:
    once = normalize_code(code)

    assert normalize_code(once) == once


def test_three_spellings_of_one_code_become_one() -> None:
    assert normalize_code("91") == normalize_code("91m") == normalize_code("\033[91m") == "91"


@pytest.mark.parametrize("code, error_name, builtin_error", REFUSED)
def test_refuses_everything_else_with_a_named_error(code: object, error_name: str, builtin_error: type) -> None:
    with pytest.raises(ParamError) as caught:
        normalize_code(code)

    assert caught.value.error_name == error_name
    assert isinstance(caught.value, builtin_error)
