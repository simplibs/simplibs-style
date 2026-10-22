from typing import Any
# Outers
from .validations import raise_color_not_int_error, raise_color_out_of_range_error


def require_color_value(
    value: Any,
    label: str,
) -> None:
    """Require a color value to be an integer from 0 to 255.

    Args:
        value: The value to check.
        label: The name shown in the failure card (`"n"`, `"r"`, `"g"`, `"b"`).

    Raises:
        ParamError: If `value` is not an integer (a `bool` is not), or lies
            outside 0-255.
    """

    # 1. A color value is an integer; True and False are not numbers here
    if not isinstance(value, int) or isinstance(value, bool):
        raise_color_not_int_error(label, value)

    # 2. One byte: 0 to 255
    if not 0 <= value <= 255:
        raise_color_out_of_range_error(label, value)


_DESIGN_NOTES = """
# require_color_value — The One Check Behind Every Number

## Purpose
`color_256` (one number) and `color_rgb` (three numbers) accept the same
kind of value. The check is written once, with the label passed in so the
card names the parameter that failed.

## Type Before Range
Comparing a string with a number raises a `TypeError` from deep inside
Python. Checking the type first turns that into a card that says what was
expected.

## `bool` Is Refused
`True` is an `int` in Python and would pass the range check, then be written
into the sequence as the text `True`.
"""
