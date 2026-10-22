# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_YELLOW = StyleDefiner(ANSI.FG_BRIGHT_YELLOW)
"""Bright yellow text.

Style:
    Text color 93 (`\\033[93m`).

Example:
    print(BRIGHT_YELLOW("Something happened"))
    # Writes the text in bright yellow.

Note:
    Stronger than `YELLOW` on most themes. Needs a terminal with bright colors (almost all).
"""
