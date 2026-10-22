# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_CYAN = StyleDefiner(ANSI.FG_BRIGHT_CYAN)
"""Bright cyan text.

Style:
    Text color 96 (`\\033[96m`).

Example:
    print(BRIGHT_CYAN("Something happened"))
    # Writes the text in bright cyan.

Note:
    Stronger than `CYAN` on most themes. Needs a terminal with bright colors (almost all).
"""
