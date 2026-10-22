from typing import Any
# Inners
from .patterns import HEX_COLOR_PATTERN


def parse_hex_color(
    value: Any,
) -> tuple[int, int, int] | None:
    """Read the red, green and blue channels out of a hex color string.

    Args:
        value: Any value; only a string such as `"#ff8800"`, `"ff8800"`,
            `"#f80"` or `"f80"` is a hex color.

    Returns:
        The channels `(r, g, b)`, each 0-255, or `None` if `value` is not a
        hex color string. Never raises.
    """

    # 1. Only a string can be a hex color
    if not isinstance(value, str):
        return None

    # 2. The text must have exactly the shape of a hex color
    match = HEX_COLOR_PATTERN.fullmatch(value)
    if match is None:
        return None

    # 3. The short form doubles every digit: "f80" means "ff8800"
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(digit * 2 for digit in digits)

    # 4. Two digits per channel
    return int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)


_DESIGN_NOTES = """
# parse_hex_color — Text In, Three Numbers Out

## Purpose
The only place that knows what a hex color means. `color_hex` asks it and
decides what to do with a `None`.

## Returns None Instead of Raising
The same split as `to_path` in `simplibs-path`: the helper answers, the
caller chooses the card. A wrong type and a wrong text both give `None`;
the raiser tells them apart for the message.

## Why Not `int(text, 16)` on the Whole String
`int("1_0", 16)`, `int(" ff", 16)` and `int("+ff", 16)` all succeed. The
pattern is checked first, so only plain hex digits ever reach `int`.
"""
