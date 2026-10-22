import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.base_class._helpers.validations import raise_invalid_ansi_format_error


@pytest.mark.parametrize("code", ["\033[2J", "\033[10;5H", "\033[91", "\033[", "\033[K"])
def test_raise_invalid_ansi_format_error_contract(subtests, code) -> None:
    """Verify raise_invalid_ansi_format_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_invalid_ansi_format_error,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="STYLE_INVALID_ANSI_FORMAT",
        label="style code",
        expected="A complete sequence such as '\\033[91m', or a bare code such as '91'.",
        value=code,
        problem=(
            "The code starts like an ANSI escape sequence but does not end with 'm'.",
            "Only style sequences (ending with 'm') are supported.",
        ),
        how_to_fix=(
            "Add the closing 'm' to the sequence.",
            "Or pass the bare number without the escape prefix.",
        ),
        exception=ValueError,
        verbose=False,
    )
