# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_WHITE import BRIGHT_WHITE


BRIGHT_WHITE_BOLD = BRIGHT_WHITE + BOLD
"""Bold bright white text.

Style:
    `BRIGHT_WHITE + BOLD`: codes 97 and 1 (`\\033[97;1m`).

Example:
    print(BRIGHT_WHITE_BOLD("Something happened"))
    # Writes the text in bold bright white.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
