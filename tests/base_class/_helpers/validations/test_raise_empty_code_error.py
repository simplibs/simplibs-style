import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.base_class._helpers.validations import raise_empty_code_error


@pytest.mark.parametrize("code", ["", " ", "   ", "\t", "m", "\033[m"])
def test_raise_empty_code_error_contract(subtests, code) -> None:
    """Verify raise_empty_code_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_empty_code_error,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="STYLE_EMPTY_CODE",
        label="style code",
        expected="A code such as '91', '91m' or '\\033[91m'.",
        value=code,
        problem="The code has no digits in it.",
        how_to_fix="Put the number of the code in front of the 'm' or the closing bracket.",
        exception=ValueError,
        verbose=False,
    )
