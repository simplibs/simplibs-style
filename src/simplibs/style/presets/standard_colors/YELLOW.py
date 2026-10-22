# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


YELLOW = StyleDefiner(ANSI.FG_YELLOW)
"""Yellow text.

Style:
    Text color 33 (`\\033[33m`).

Example:
    print(YELLOW("Something happened"))
    # Writes the text in yellow.

Note:
    The exact shade depends on the terminal theme. For a stronger color use `BRIGHT_YELLOW`.
"""
