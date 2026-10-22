# Outers
from ..attributes import BOLD
# Inners
from .BLUE import BLUE


BLUE_BOLD = BLUE + BOLD
"""Bold blue text.

Style:
    `BLUE + BOLD`: codes 34 and 1 (`\\033[34;1m`).

Example:
    print(BLUE_BOLD("Something happened"))
    # Writes the text in bold blue.

Note:
    On many terminals bold also brightens the color.
"""
