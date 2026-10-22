# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BLACK = StyleDefiner(ANSI.BG_BLACK)
"""Black background.

Style:
    Background color 40 (`\\033[40m`).

Example:
    print(BG_BLACK("ALERT"))
    # Writes the text on a black background.

Note:
    Set a text color too, so the text stays readable: `BG_BLACK + BRIGHT_WHITE`.
"""
