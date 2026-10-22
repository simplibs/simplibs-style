# Outers
from ..attributes import BOLD
# Inners
from .BLACK import BLACK


BLACK_BOLD = BLACK + BOLD
"""Bold black text.

Style:
    `BLACK + BOLD`: codes 30 and 1 (`\\033[30;1m`).

Example:
    print(BLACK_BOLD("Something happened"))
    # Writes the text in bold black.

Note:
    On many terminals bold also brightens the color.
"""
