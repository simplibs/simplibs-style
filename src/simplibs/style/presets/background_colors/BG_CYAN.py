# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_CYAN = StyleDefiner(ANSI.BG_CYAN)
"""Cyan background.

Style:
    Background color 46 (`\\033[46m`).

Example:
    print(BG_CYAN("ALERT"))
    # Writes the text on a cyan background.

Note:
    Set a text color too, so the text stays readable: `BG_CYAN + BRIGHT_WHITE`.
"""
