# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_RED = StyleDefiner(ANSI.BG_RED)
"""Red background.

Style:
    Background color 41 (`\\033[41m`).

Example:
    print(BG_RED("ALERT"))
    # Writes the text on a red background.

Note:
    Set a text color too, so the text stays readable: `BG_RED + BRIGHT_WHITE`.
"""
