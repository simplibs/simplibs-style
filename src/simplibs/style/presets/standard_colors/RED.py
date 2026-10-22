# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


RED = StyleDefiner(ANSI.FG_RED)
"""Red text.

Style:
    Text color 31 (`\\033[31m`).

Example:
    print(RED("Something happened"))
    # Writes the text in red.

Note:
    The exact shade depends on the terminal theme. For a stronger color use `BRIGHT_RED`.
"""
