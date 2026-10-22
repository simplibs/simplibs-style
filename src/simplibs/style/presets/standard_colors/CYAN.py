# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


CYAN = StyleDefiner(ANSI.FG_CYAN)
"""Cyan text.

Style:
    Text color 36 (`\\033[36m`).

Example:
    print(CYAN("Something happened"))
    # Writes the text in cyan.

Note:
    The exact shade depends on the terminal theme. For a stronger color use `BRIGHT_CYAN`.
"""
