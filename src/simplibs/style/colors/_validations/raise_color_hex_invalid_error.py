from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_color_hex_invalid_error(
    value: Any,
) -> NoReturn:
    """Raise ParamError when a value is not a hex color string.

    Args:
        value: The rejected value.
    """

    # 1. A wrong kind of value is a TypeError, a wrong text is a ValueError
    is_text = isinstance(value, str)
    problem = (
        "The text is not a hex color."
        if is_text
        else "A hex color is written as text."
    )

    # 2. Raise structured ParamError
    raise ParamError(
        error_name="STYLE_COLOR_HEX_INVALID",
        label="hex color",
        value=value,
        problem=problem,
        expected="Six or three hex digits, with or without '#': '#ff8800', 'ff8800', '#f80'.",
        how_to_fix=(
            "Use only the digits 0-9 and the letters a-f.",
            "Remove spaces, a '0x' prefix and any alpha channel.",
        ),
        exception=ValueError if is_text else TypeError,
    )


_DESIGN_NOTES = """
# raise_color_hex_invalid_error — Almost a Color

## Purpose
`"#ff88"`, `"#gg8800"` and `"#ff8800ff"` all look close and none works. The
card shows the accepted spellings.

## One Card, Two Exceptions
A value that is not text wraps `TypeError`; text of the wrong shape wraps
`ValueError`, the same split as in `raise_list_start_negative_error` of
`simplibs-markdown`.
"""
