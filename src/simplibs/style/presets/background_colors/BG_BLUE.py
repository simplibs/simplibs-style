# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BLUE = StyleDefiner(ANSI.BG_BLUE)
"""Blue background.

Style:
    Background color 44 (`\\033[44m`).

Example:
    print(BG_BLUE("ALERT"))
    # Writes the text on a blue background.

Note:
    Set a text color too, so the text stays readable: `BG_BLUE + BRIGHT_WHITE`.
"""
