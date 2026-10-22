# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


MAGENTA = StyleDefiner(ANSI.FG_MAGENTA)
"""Magenta text.

Style:
    Text color 35 (`\\033[35m`).

Example:
    print(MAGENTA("Something happened"))
    # Writes the text in magenta.

Note:
    The exact shade depends on the terminal theme. For a stronger color use `BRIGHT_MAGENTA`.
"""
