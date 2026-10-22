import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.colors._helpers.validations import raise_color_background_not_bool_error


@pytest.mark.parametrize("value", ["no", "yes", "", 1, 0, None, 3.14, [], {"a": 1}])
def test_raise_color_background_not_bool_error_contract(subtests, value) -> None:
    """Verify raise_color_background_not_bool_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_color_background_not_bool_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="STYLE_COLOR_BACKGROUND_NOT_BOOL",
        label="background",
        expected="A bool: True or False.",
        value=value,
        problem="Only True or False can choose between a text and a background color.",
        how_to_fix=(
            "Pass True for a background color.",
            "Leave `background` out for a text color.",
        ),
        exception=TypeError,
        verbose=False,
    )
