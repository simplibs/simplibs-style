import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.settings._classes.validations import raise_styles_override_used_as_bool_error


def test_raise_styles_override_used_as_bool_error_contract(subtests) -> None:
    """Verify raise_styles_override_used_as_bool_error produces a well-formed ParamError card."""

    assert_exception_function(
        subtests,
        raise_styles_override_used_as_bool_error,
        invalid_params=(),
        exception_type=ParamError,
        error_name="STYLE_OVERRIDE_USED_AS_BOOL",
        label="styles override",
        expected="A `with` statement, e.g. `with styles_enabled():`.",
        problem=(
            "`styles_enabled()` and `styles_disabled()` are blocks for a `with` statement, not yes/no questions.",
            "Used as a condition they would be always true.",
        ),
        how_to_fix=(
            "Use `get_styles_enabled()` to ask whether styles are on.",
            "Use `with styles_enabled():` to force styles on for a block.",
        ),
        exception=TypeError,
        verbose=False,
    )
