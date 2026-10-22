# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_YELLOW = StyleDefiner(ANSI.BG_BRIGHT_YELLOW)
"""Bright yellow background.

Style:
    Background color 103 (`\\033[103m`).

Example:
    print(BG_BRIGHT_YELLOW("ALERT"))
    # Writes the text on a bright yellow background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_YELLOW + BLACK`.
"""
