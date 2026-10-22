# Outers
from ..attributes import BOLD
# Inners
from .YELLOW import YELLOW


YELLOW_BOLD = YELLOW + BOLD
"""Bold yellow text.

Style:
    `YELLOW + BOLD`: codes 33 and 1 (`\\033[33;1m`).

Example:
    print(YELLOW_BOLD("Something happened"))
    # Writes the text in bold yellow.

Note:
    On many terminals bold also brightens the color.
"""
