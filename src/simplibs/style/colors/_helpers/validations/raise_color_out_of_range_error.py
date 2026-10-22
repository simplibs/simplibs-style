from typing import NoReturn
from simplibs.exception import ParamError


def raise_color_out_of_range_error(
    label: str,
    value: int,
) -> NoReturn:
    """Raise ParamError when a color value is outside the range 0-255.

    Args:
        label: The name of the rejected parameter (`"n"`, `"r"`, `"g"`, `"b"`).
        value: The rejected number.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="STYLE_COLOR_OUT_OF_RANGE",
        label=label,
        value=value,
        problem="The number does not fit into one byte.",
        expected="An integer from 0 to 255.",
        how_to_fix="Pass a value between 0 and 255.",
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_color_out_of_range_error — A Byte Has 256 Values

## Purpose
One card for the palette index and for each RGB channel. A terminal does not
refuse 300; it wraps the number or shows a wrong color, and the cause stays
hidden.
"""
