# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_MAGENTA = StyleDefiner(ANSI.FG_BRIGHT_MAGENTA)
"""Bright magenta text.

Style:
    Text color 95 (`\\033[95m`).

Example:
    print(BRIGHT_MAGENTA("Something happened"))
    # Writes the text in bright magenta.

Note:
    Stronger than `MAGENTA` on most themes. Needs a terminal with bright colors (almost all).
"""
