# Outers
from ..attributes import BOLD
# Inners
from .CYAN import CYAN


CYAN_BOLD = CYAN + BOLD
"""Bold cyan text.

Style:
    `CYAN + BOLD`: codes 36 and 1 (`\\033[36;1m`).

Example:
    print(CYAN_BOLD("Something happened"))
    # Writes the text in bold cyan.

Note:
    On many terminals bold also brightens the color.
"""
