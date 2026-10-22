from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_use_style_not_bool_error(
    value: Any,
) -> NoReturn:
    """Raise ParamError when `use_style` is neither None nor a bool.

    Args:
        value: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="STYLE_USE_STYLE_NOT_BOOL",
        label="use_style",
        value=value,
        problem="Only True, False or None can decide whether this call is styled.",
        expected="True, False, or None to follow the current setting.",
        how_to_fix=(
            "Pass True to force styling, or False to force plain text.",
            "Leave `use_style` out to follow the current setting.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_use_style_not_bool_error — "no" Is Truthy

## Purpose
`RED("x", use_style="no")` would read the string as true and style the text,
the opposite of what was meant. The mistake is refused where it is made.
"""
