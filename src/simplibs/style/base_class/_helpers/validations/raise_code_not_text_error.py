from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_code_not_text_error(
    code: Any,
) -> NoReturn:
    """Raise ParamError when a style code is not a string.

    Args:
        code: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="STYLE_CODE_NOT_TEXT",
        label="style code",
        value=code,
        problem="A style code is written as text, not as another type.",
        expected="A string such as '91', '91m' or '\\033[91m', or another StyleDefiner.",
        how_to_fix=(
            "Wrap the number in quotes: '91' instead of 91.",
            "Use `color_256` or `color_rgb` to build a color from numbers.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_code_not_text_error — 91 Is Not "91"

## Purpose
Codes are joined with semicolons into one sequence, so they are text. A
number would fail deep inside the string handling with a message about
`startswith`; this card names the real mistake.
"""
