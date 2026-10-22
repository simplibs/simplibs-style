# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_CYAN = StyleDefiner(ANSI.BG_BRIGHT_CYAN)
"""Bright cyan background.

Style:
    Background color 106 (`\\033[106m`).

Example:
    print(BG_BRIGHT_CYAN("ALERT"))
    # Writes the text on a bright cyan background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_CYAN + BLACK`.
"""
