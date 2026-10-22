# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_WHITE = StyleDefiner(ANSI.BG_WHITE)
"""White background.

Style:
    Background color 47 (`\\033[47m`).

Example:
    print(BG_WHITE("ALERT"))
    # Writes the text on a white background.

Note:
    Set a text color too, so the text stays readable: `BG_WHITE + BRIGHT_WHITE`.
"""
