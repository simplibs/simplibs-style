# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


GREEN = StyleDefiner(ANSI.FG_GREEN)
"""Green text.

Style:
    Text color 32 (`\\033[32m`).

Example:
    print(GREEN("Something happened"))
    # Writes the text in green.

Note:
    The exact shade depends on the terminal theme. For a stronger color use `BRIGHT_GREEN`.
"""
