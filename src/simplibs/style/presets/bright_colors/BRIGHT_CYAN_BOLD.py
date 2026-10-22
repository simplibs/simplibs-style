# Outers
from ..attributes import BOLD
# Inners
from .BRIGHT_CYAN import BRIGHT_CYAN


BRIGHT_CYAN_BOLD = BRIGHT_CYAN + BOLD
"""Bold bright cyan text.

Style:
    `BRIGHT_CYAN + BOLD`: codes 96 and 1 (`\\033[96;1m`).

Example:
    print(BRIGHT_CYAN_BOLD("Something happened"))
    # Writes the text in bold bright cyan.

Note:
    The strongest text of this color; the log presets `SUCCESS`, `WARNING` and `ERROR` use it.
"""
