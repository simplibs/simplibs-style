# Outers
from ...constants import ANSI
# Inners
from .validations import raise_color_background_not_bool_error


def choose_color_introducer(
    background: bool,
) -> str:
    """Choose the code that introduces an extended color: text or background.

    Args:
        background: True for a background color, False for a text color.

    Returns:
        `"48"` for a background color, `"38"` for a text color.

    Raises:
        ParamError: If `background` is not a bool.
    """

    # 1. Only a real bool picks a side
    if not isinstance(background, bool):
        raise_color_background_not_bool_error(background)

    # 2. Background colors start with 48, text colors with 38
    return ANSI.BG_EXTENDED if background else ANSI.FG_EXTENDED


_DESIGN_NOTES = """
# choose_color_introducer — Text or Background

## Purpose
`38` and `48` begin every extended color; only the number differs between
the two sides. The choice, and the check of the flag that makes it, are
shared by every color builder.

## A Strict Bool
`background="no"` is a non-empty string, which is truthy, and would paint
the background. Refused, like `use_style` in `StyleDefiner`.
"""
