# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_WHITE = StyleDefiner(ANSI.FG_BRIGHT_WHITE)
"""Bright white text.

Style:
    Text color 97 (`\\033[97m`).

Example:
    print(BRIGHT_WHITE("Something happened"))
    # Writes the text in bright white.

Note:
    Stronger than `WHITE` on most themes. Needs a terminal with bright colors (almost all).
"""
