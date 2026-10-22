# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_GREEN import BRIGHT_GREEN


BRIGHT_GREEN_BOLD = BRIGHT_GREEN + BOLD
"""Bold bright green text.

Style:
    `BRIGHT_GREEN + BOLD`: codes 92 and 1 (`\\033[92;1m`).

Example:
    print(BRIGHT_GREEN_BOLD("Something happened"))
    # Writes the text in bold bright green.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
