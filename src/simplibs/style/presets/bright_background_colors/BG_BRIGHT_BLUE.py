# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_BLUE = StyleDefiner(ANSI.BG_BRIGHT_BLUE)
"""Bright blue background.

Style:
    Background color 104 (`\\033[104m`).

Example:
    print(BG_BRIGHT_BLUE("ALERT"))
    # Writes the text on a bright blue background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_BLUE + BLACK`.
"""
