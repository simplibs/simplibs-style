# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_MAGENTA = StyleDefiner(ANSI.BG_BRIGHT_MAGENTA)
"""Bright magenta background.

Style:
    Background color 105 (`\\033[105m`).

Example:
    print(BG_BRIGHT_MAGENTA("ALERT"))
    # Writes the text on a bright magenta background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_MAGENTA + BLACK`.
"""
