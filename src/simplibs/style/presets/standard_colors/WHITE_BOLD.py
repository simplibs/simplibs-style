# Outers
from ..attributes import BOLD
# Inners
from .WHITE import WHITE


WHITE_BOLD = WHITE + BOLD
"""Bold white text.

Style:
    `WHITE + BOLD`: codes 37 and 1 (`\\033[37;1m`).

Example:
    print(WHITE_BOLD("Something happened"))
    # Writes the text in bold white.

Note:
    On many terminals bold also brightens the color.
"""
