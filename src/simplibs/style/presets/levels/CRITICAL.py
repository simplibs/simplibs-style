# Outers
from ..attributes import BOLD
from ..background_colors import BG_RED
from ..bright_colors import BRIGHT_WHITE


CRITICAL = BG_RED + BRIGHT_WHITE + BOLD
"""Style for critical failures: bold bright white text on red.

Style:
    `BG_RED + BRIGHT_WHITE + BOLD`: codes 41, 97 and 1 (`\\033[41;97;1m`).

Example:
    print(CRITICAL("database is unreachable"))
    # Writes the message in bold white on a red background.

Note:
    Stands out from `ERROR` even when the colors of the text are hard to tell apart.
"""
