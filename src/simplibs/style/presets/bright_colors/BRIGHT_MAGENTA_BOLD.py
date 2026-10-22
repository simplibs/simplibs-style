# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_MAGENTA import BRIGHT_MAGENTA


BRIGHT_MAGENTA_BOLD = BRIGHT_MAGENTA + BOLD
"""Bold bright magenta text.

Style:
    `BRIGHT_MAGENTA + BOLD`: codes 95 and 1 (`\\033[95;1m`).

Example:
    print(BRIGHT_MAGENTA_BOLD("Something happened"))
    # Writes the text in bold bright magenta.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
