import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.settings._validations import raise_styles_enabled_not_bool_error


_EXPECTED = "A bool: True or False."
_HOW_TO_FIX = (
    "Pass True to style text, or False to leave it plain.",
    "Convert other values with bool() first, if that is what you mean.",
)


@pytest.mark.parametrize(
    "value",
    ["yes", "no", "", 0, 1, None, [], {}, object()],
)
def test_raise_styles_enabled_not_bool_error(subtests, value) -> None:
    """Verify a non-bool value raises ParamError wrapping TypeError."""
    assert_exception_function(
        subtests,
        raise_styles_enabled_not_bool_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="STYLE_STYLES_ENABLED_NOT_BOOL",
        label="styles enabled",
        expected=_EXPECTED,
        value=value,
        problem="Only True or False can switch styling on or off.",
        how_to_fix=_HOW_TO_FIX,
        exception=TypeError,
        verbose=False,
    )