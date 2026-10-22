# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_RED import BRIGHT_RED


BRIGHT_RED_BOLD = BRIGHT_RED + BOLD
"""Bold bright red text.

Style:
    `BRIGHT_RED + BOLD`: codes 91 and 1 (`\\033[91;1m`).

Example:
    print(BRIGHT_RED_BOLD("Something happened"))
    # Writes the text in bold bright red.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
