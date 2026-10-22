# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_RED = StyleDefiner(ANSI.BG_BRIGHT_RED)
"""Bright red background.

Style:
    Background color 101 (`\\033[101m`).

Example:
    print(BG_BRIGHT_RED("ALERT"))
    # Writes the text on a bright red background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_RED + BLACK`.
"""
