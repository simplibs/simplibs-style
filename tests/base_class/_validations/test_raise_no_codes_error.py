import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.base_class._validations import raise_no_codes_error


def test_raise_no_codes_error_contract(subtests) -> None:
    """Verify raise_no_codes_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_no_codes_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="STYLE_NO_CODES",
        label="style codes",
        expected="At least one code or another StyleDefiner.",
        problem="A style needs at least one code.",
        how_to_fix=(
            "Pass a code such as '91', or a ready style such as RED.",
            "Use a preset like BOLD when you do not need a custom style.",
        ),
        exception=ValueError,
        verbose=False,
    )
