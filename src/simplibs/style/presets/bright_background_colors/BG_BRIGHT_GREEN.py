# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_GREEN = StyleDefiner(ANSI.BG_BRIGHT_GREEN)
"""Bright green background.

Style:
    Background color 102 (`\\033[102m`).

Example:
    print(BG_BRIGHT_GREEN("ALERT"))
    # Writes the text on a bright green background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_GREEN + BLACK`.
"""
