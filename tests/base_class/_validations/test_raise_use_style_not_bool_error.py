import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.base_class._validations import raise_use_style_not_bool_error


@pytest.mark.parametrize("value", ["no", "yes", "", 1, 0, 3.14, [], ["x"], {"a": 1}])
def test_raise_use_style_not_bool_error_contract(subtests, value) -> None:
    """Verify raise_use_style_not_bool_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_use_style_not_bool_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="STYLE_USE_STYLE_NOT_BOOL",
        label="use_style",
        expected="True, False, or None to follow the current setting.",
        value=value,
        problem="Only True, False or None can decide whether this call is styled.",
        how_to_fix=(
            "Pass True to force styling, or False to force plain text.",
            "Leave `use_style` out to follow the current setting.",
        ),
        exception=TypeError,
        verbose=False,
    )
