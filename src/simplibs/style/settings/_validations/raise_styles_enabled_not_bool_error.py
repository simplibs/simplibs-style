from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_styles_enabled_not_bool_error(
    value: Any,
) -> NoReturn:
    """Raise ParamError when the styling switch is given something other than a bool.

    Args:
        value: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="STYLE_STYLES_ENABLED_NOT_BOOL",
        label="styles enabled",
        value=value,
        problem="Only True or False can switch styling on or off.",
        expected="A bool: True or False.",
        how_to_fix=(
            "Pass True to style text, or False to leave it plain.",
            "Convert other values with bool() first, if that is what you mean.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_styles_enabled_not_bool_error — A Switch With Three Positions

## Purpose
`set_styles_enabled("no")` would store a non-empty string and turn styling
on. The mistake would show up as colors where there should be none, far from
the call that caused it.
"""
