# Outers
from ..base_class import StyleDefiner
# Inners
from .color_rgb import color_rgb
from ._helpers import parse_hex_color
from ._validations import raise_color_hex_invalid_error


def color_hex(
    value: str,
    *,
    background: bool = False,
) -> StyleDefiner:
    """Build a style for a true-color value written as a hex string.

    Args:
        value: Six hex digits (`"ff8800"`) or three (`"f80"`, each digit
            doubled), with or without a leading `#`.
        background: If True, the color is applied to the background instead
            of the text.

    Returns:
        A `StyleDefiner` equal to `color_rgb(r, g, b)` of the same color.

    Raises:
        ParamError: If `value` is not a hex color string, or `background`
            is not a bool.

    Example:
        ORANGE = color_hex("#ff8800")
        print(ORANGE("Orange text"))

        ORANGE_SHORT = color_hex("f80")
    """

    # 1. Read the channels out of the text
    channels = parse_hex_color(value)
    if channels is None:
        raise_color_hex_invalid_error(value)

    # 2. A hex color is an RGB color written differently
    return color_rgb(*channels, background=background)


_DESIGN_NOTES = """
# color_hex — The Way Colors Are Copied From Design Tools

## Purpose
Colors usually arrive as `#ff8800` from a design, a stylesheet or a color
picker. Converting them to three numbers by hand is the kind of step that
goes wrong; the builder takes the text as it is.

## A Thin Layer
It only parses; the sequence is built by `color_rgb`, so the two cannot
drift apart.

## Strict on Purpose
No whitespace, no `0x` prefix, no names such as `"orange"`, no `#rrggbbaa`:
a terminal has no transparency, and every extra spelling is one more way for
a typo to be accepted silently.
"""
