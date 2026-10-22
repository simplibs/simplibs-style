# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_BLUE = StyleDefiner(ANSI.FG_BRIGHT_BLUE)
"""Bright blue text.

Style:
    Text color 94 (`\\033[94m`).

Example:
    print(BRIGHT_BLUE("Something happened"))
    # Writes the text in bright blue.

Note:
    Stronger than `BLUE` on most themes. Needs a terminal with bright colors (almost all).
"""
