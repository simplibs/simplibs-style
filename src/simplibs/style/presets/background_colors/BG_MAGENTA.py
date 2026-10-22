# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_MAGENTA = StyleDefiner(ANSI.BG_MAGENTA)
"""Magenta background.

Style:
    Background color 45 (`\\033[45m`).

Example:
    print(BG_MAGENTA("ALERT"))
    # Writes the text on a magenta background.

Note:
    Set a text color too, so the text stays readable: `BG_MAGENTA + BRIGHT_WHITE`.
"""
