import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.colors._helpers.validations import raise_color_not_int_error


@pytest.mark.parametrize("label", ["n", "r", "g", "b"])
@pytest.mark.parametrize("value", ["208", 3.5, None, True, False, [208], b"208"])
def test_raise_color_not_int_error_contract(subtests, label, value) -> None:
    """Verify raise_color_not_int_error names the parameter and produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_color_not_int_error,
        invalid_params=(label, value),
        exception_type=ParamError,
        error_name="STYLE_COLOR_NOT_INT",
        label=label,
        expected="An integer from 0 to 255.",
        value=value,
        problem="A color value is a whole number, not another type.",
        how_to_fix=(
            "Pass a number such as 208, not text such as '208'.",
            "Use `color_hex` when the color is written as a hex string.",
        ),
        exception=TypeError,
        verbose=False,
    )
