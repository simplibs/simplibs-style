# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_YELLOW = StyleDefiner(ANSI.BG_YELLOW)
"""Yellow background.

Style:
    Background color 43 (`\\033[43m`).

Example:
    print(BG_YELLOW("ALERT"))
    # Writes the text on a yellow background.

Note:
    Set a text color too, so the text stays readable: `BG_YELLOW + BRIGHT_WHITE`.
"""
