# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_BLACK import BRIGHT_BLACK


BRIGHT_BLACK_BOLD = BRIGHT_BLACK + BOLD
"""Bold bright black text.

Style:
    `BRIGHT_BLACK + BOLD`: codes 90 and 1 (`\\033[90;1m`).

Example:
    print(BRIGHT_BLACK_BOLD("Something happened"))
    # Writes the text in bold bright black.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
