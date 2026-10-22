# Outers
from ..constants import ANSI
from ..base_class import StyleDefiner
# Inners
from ._helpers import choose_color_introducer, require_color_value


def color_256(
    n: int,
    *,
    background: bool = False,
) -> StyleDefiner:
    """Build a style for an entry of the 256-color palette.

    Args:
        n: The palette index, 0-255. 0-7 are the standard colors, 8-15 the
            bright ones, 16-231 a 6x6x6 color cube and 232-255 a gray ramp.
        background: If True, the color is applied to the background instead
            of the text.

    Returns:
        A `StyleDefiner` with the code `38;5;N` (text) or `48;5;N` (background).

    Raises:
        ParamError: If `n` is not an integer from 0 to 255, or `background`
            is not a bool.

    Example:
        ORANGE = color_256(208)
        print(ORANGE("Orange text"))
    """

    # 1. Validate the palette index
    require_color_value(n, "n")

    # 2. Foreground or background
    introducer = choose_color_introducer(background)

    # 3. Build the style from the three parts of the code
    return StyleDefiner(f"{introducer};{ANSI.EXTENDED_256};{n}")


_DESIGN_NOTES = """
# color_256 — One of 256 Named-by-Number Colors

## Purpose
The middle step between the sixteen preset colors and full RGB: widely
supported (every terminal that has colors beyond the basic sixteen), and a
single number is easy to write down and to share.

## Same Rules as `color_rgb`
Both builders share `require_color_value` and `choose_color_introducer`, so
a `bool` is refused as a number and `background` must be a real `bool` in
both.
"""
