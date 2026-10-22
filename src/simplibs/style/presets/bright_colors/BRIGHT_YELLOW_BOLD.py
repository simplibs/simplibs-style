# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_YELLOW import BRIGHT_YELLOW


BRIGHT_YELLOW_BOLD = BRIGHT_YELLOW + BOLD
"""Bold bright yellow text.

Style:
    `BRIGHT_YELLOW + BOLD`: codes 93 and 1 (`\\033[93;1m`).

Example:
    print(BRIGHT_YELLOW_BOLD("Something happened"))
    # Writes the text in bold bright yellow.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
