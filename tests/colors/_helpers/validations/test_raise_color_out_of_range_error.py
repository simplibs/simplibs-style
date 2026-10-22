import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.colors._helpers.validations import raise_color_out_of_range_error


@pytest.mark.parametrize("label", ["n", "r", "g", "b"])
@pytest.mark.parametrize("value", [-1, -255, 256, 300, 10 ** 6])
def test_raise_color_out_of_range_error_contract(subtests, label, value) -> None:
    """Verify raise_color_out_of_range_error names the parameter and produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_color_out_of_range_error,
        invalid_params=(label, value),
        exception_type=ParamError,
        error_name="STYLE_COLOR_OUT_OF_RANGE",
        label=label,
        expected="An integer from 0 to 255.",
        value=value,
        problem="The number does not fit into one byte.",
        how_to_fix="Pass a value between 0 and 255.",
        exception=ValueError,
        verbose=False,
    )
