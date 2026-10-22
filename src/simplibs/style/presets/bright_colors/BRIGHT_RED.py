# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_RED = StyleDefiner(ANSI.FG_BRIGHT_RED)
"""Bright red text.

Style:
    Text color 91 (`\\033[91m`).

Example:
    print(BRIGHT_RED("Something happened"))
    # Writes the text in bright red.

Note:
    Stronger than `RED` on most themes. Needs a terminal with bright colors (almost all).
"""
