# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_GREEN = StyleDefiner(ANSI.FG_BRIGHT_GREEN)
"""Bright green text.

Style:
    Text color 92 (`\\033[92m`).

Example:
    print(BRIGHT_GREEN("Something happened"))
    # Writes the text in bright green.

Note:
    Stronger than `GREEN` on most themes. Needs a terminal with bright colors (almost all).
"""
