import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.base_class._helpers.validations import raise_code_not_text_error


@pytest.mark.parametrize("code", [91, 3.14, None, True, ["91"], b"91", {"a": 1}])
def test_raise_code_not_text_error_contract(subtests, code) -> None:
    """Verify raise_code_not_text_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_code_not_text_error,
        invalid_params=(code,),
        exception_type=ParamError,
        error_name="STYLE_CODE_NOT_TEXT",
        label="style code",
        expected="A string such as '91', '91m' or '\\033[91m', or another StyleDefiner.",
        value=code,
        problem="A style code is written as text, not as another type.",
        how_to_fix=(
            "Wrap the number in quotes: '91' instead of 91.",
            "Use `color_256` or `color_rgb` to build a color from numbers.",
        ),
        exception=TypeError,
        verbose=False,
    )
