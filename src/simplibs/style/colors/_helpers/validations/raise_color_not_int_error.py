from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_color_not_int_error(
    label: str,
    value: Any,
) -> NoReturn:
    """Raise ParamError when a color value is not an integer.

    Args:
        label: The name of the rejected parameter (`"n"`, `"r"`, `"g"`, `"b"`).
        value: The rejected value.
    """

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="STYLE_COLOR_NOT_INT",
        label=label,
        value=value,
        problem="A color value is a whole number, not another type.",
        expected="An integer from 0 to 255.",
        how_to_fix=(
            "Pass a number such as 208, not text such as '208'.",
            "Use `color_hex` when the color is written as a hex string.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_color_not_int_error — "208" Is Not 208

## Purpose
Names the real mistake (the type) before the range is even looked at. A
`bool` lands here too, because `True` is not a color.
"""
