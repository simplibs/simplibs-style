# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BLUE = StyleDefiner(ANSI.FG_BLUE)
"""Blue text.

Style:
    Text color 34 (`\\033[34m`).

Example:
    print(BLUE("Something happened"))
    # Writes the text in blue.

Note:
    The exact shade depends on the terminal theme. For a stronger color use `BRIGHT_BLUE`.
"""
