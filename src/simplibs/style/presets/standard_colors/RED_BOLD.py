# Outers
from ..attributes import BOLD
# Inners
from .RED import RED


RED_BOLD = RED + BOLD
"""Bold red text.

Style:
    `RED + BOLD`: codes 31 and 1 (`\\033[31;1m`).

Example:
    print(RED_BOLD("Something happened"))
    # Writes the text in bold red.

Note:
    On many terminals bold also brightens the color.
"""
