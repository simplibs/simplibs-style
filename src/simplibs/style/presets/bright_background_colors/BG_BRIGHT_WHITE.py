# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_WHITE = StyleDefiner(ANSI.BG_BRIGHT_WHITE)
"""Bright white background.

Style:
    Background color 107 (`\\033[107m`).

Example:
    print(BG_BRIGHT_WHITE("ALERT"))
    # Writes the text on a bright white background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_WHITE + BLACK`.
"""
