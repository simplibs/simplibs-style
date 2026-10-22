# Outers
from ..attributes import BOLD
from ..bright_colors import BRIGHT_RED


ERROR = BRIGHT_RED + BOLD
"""Style for errors: bold bright red text.

Style:
    `BRIGHT_RED + BOLD`: codes 91 and 1 (`\\033[91;1m`).

Example:
    print(ERROR("could not open the file"))
    # Writes the message in bold bright red.

Note:
    Equal to `BRIGHT_RED_BOLD`; the name says what it is for.
"""
