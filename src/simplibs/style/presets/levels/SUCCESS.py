# Outers
from ..attributes import BOLD
from ..bright_colors import BRIGHT_GREEN


SUCCESS = BRIGHT_GREEN + BOLD
"""Style for success messages: bold bright green text.

Style:
    `BRIGHT_GREEN + BOLD`: codes 92 and 1 (`\\033[92;1m`).

Example:
    print(SUCCESS("all tests passed"))
    # Writes the message in bold bright green.

Note:
    Equal to `BRIGHT_GREEN_BOLD`; the name says what it is for.
"""
