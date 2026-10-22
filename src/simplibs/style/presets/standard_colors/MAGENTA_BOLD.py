# Outers
from ..attributes import BOLD
# Inners
from .MAGENTA import MAGENTA


MAGENTA_BOLD = MAGENTA + BOLD
"""Bold magenta text.

Style:
    `MAGENTA + BOLD`: codes 35 and 1 (`\\033[35;1m`).

Example:
    print(MAGENTA_BOLD("Something happened"))
    # Writes the text in bold magenta.

Note:
    On many terminals bold also brightens the color.
"""
