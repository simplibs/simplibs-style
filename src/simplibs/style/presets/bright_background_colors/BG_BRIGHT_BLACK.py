# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_BRIGHT_BLACK = StyleDefiner(ANSI.BG_BRIGHT_BLACK)
"""Bright black background.

Style:
    Background color 100 (`\\033[100m`).

Example:
    print(BG_BRIGHT_BLACK("ALERT"))
    # Writes the text on a bright black background.

Note:
    Set a text color too, so the text stays readable: `BG_BRIGHT_BLACK + BLACK`.
"""
