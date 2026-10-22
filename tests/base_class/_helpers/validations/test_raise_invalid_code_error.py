import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.base_class._helpers.validations import raise_invalid_code_error


@pytest.mark.parametrize("code", ["9 1", "91;", ";91", "9;;1", "abc", "-5", "+1", "91m", "9.1", "38;5;"])
def test_raise_invalid_code_error_contract(subtests, code) -> None:
    """Verify raise_invalid_code_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_invalid_code_error,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="STYLE_INVALID_CODE",
        label="style code",
        expected="Digits joined by semicolons, e.g. '91' or '38;5;208'.",
        value=code,
        problem=(
            "The code contains something other than the digits 0-9 and single semicolons.",
            "Spaces, letters, signs and doubled or trailing semicolons are not allowed.",
        ),
        how_to_fix=(
            "Remove everything but the digits and the separating semicolons.",
            "Use `color_256` or `color_rgb` to build the multi-part color codes.",
        ),
        exception=ValueError,
        verbose=False,
    )
