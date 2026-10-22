# Outers
from ..attributes import BOLD
# Inners
from .GREEN import GREEN


GREEN_BOLD = GREEN + BOLD
"""Bold green text.

Style:
    `GREEN + BOLD`: codes 32 and 1 (`\\033[32;1m`).

Example:
    print(GREEN_BOLD("Something happened"))
    # Writes the text in bold green.

Note:
    On many terminals bold also brightens the color.
"""
