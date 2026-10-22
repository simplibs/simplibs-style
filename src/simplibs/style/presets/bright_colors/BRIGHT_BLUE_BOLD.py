# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_BLUE import BRIGHT_BLUE


BRIGHT_BLUE_BOLD = BRIGHT_BLUE + BOLD
"""Bold bright blue text.

Style:
    `BRIGHT_BLUE + BOLD`: codes 94 and 1 (`\\033[94;1m`).

Example:
    print(BRIGHT_BLUE_BOLD("Something happened"))
    # Writes the text in bold bright blue.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
