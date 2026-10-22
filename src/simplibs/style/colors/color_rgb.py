# Outers
from ..constants import ANSI
from ..base_class import StyleDefiner
# Inners
from ._helpers import choose_color_introducer, require_color_value


def color_rgb(
    r: int,
    g: int,
    b: int,
    *,
    background: bool = False,
) -> StyleDefiner:
    """Build a style for a true-color (24-bit) RGB value.

    Args:
        r: Red component, 0-255.
        g: Green component, 0-255.
        b: Blue component, 0-255.
        background: If True, the color is applied to the background instead
            of the text.

    Returns:
        A `StyleDefiner` with the code `38;2;R;G;B` (text) or `48;2;R;G;B`
        (background).

    Raises:
        ParamError: If any channel is not an integer from 0 to 255, or
            `background` is not a bool.

    Example:
        ORANGE = color_rgb(255, 136, 0)
        print(ORANGE("Orange text"))
    """

    # 1. Validate every channel
    for value, label in ((r, "r"), (g, "g"), (b, "b")):
        require_color_value(value, label)

    # 2. Foreground or background
    introducer = choose_color_introducer(background)

    # 3. Build the style from the parts of the code
    return StyleDefiner(f"{introducer};{ANSI.EXTENDED_RGB};{r};{g};{b}")


_DESIGN_NOTES = """
# color_rgb — Any Color a Terminal Can Show

## Purpose
Exact colors for terminals with true-color support (most current ones). A
terminal without it shows the nearest color it has, or none.

## Channels Are Checked One by One
The card names the failing channel (`r`, `g` or `b`) and shows its value,
instead of reporting "one of three is wrong".
"""
