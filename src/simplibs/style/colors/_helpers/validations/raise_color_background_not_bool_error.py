from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_color_background_not_bool_error(
    value: Any,
) -> NoReturn:
    """Raise ParamError when `background` is not a bool.

    Args:
        value: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="STYLE_COLOR_BACKGROUND_NOT_BOOL",
        label="background",
        value=value,
        problem="Only True or False can choose between a text and a background color.",
        expected="A bool: True or False.",
        how_to_fix=(
            "Pass True for a background color.",
            "Leave `background` out for a text color.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_color_background_not_bool_error — "no" Is Truthy

## Purpose
`color_256(208, background="no")` would read the string as true and paint the
background — the opposite of the intent, noticed only on the screen.
"""
