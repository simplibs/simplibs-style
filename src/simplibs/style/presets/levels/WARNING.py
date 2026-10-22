# Outers
from ..attributes import BOLD
from ..bright_colors import BRIGHT_YELLOW


WARNING = BRIGHT_YELLOW + BOLD
"""Style for warnings: bold bright yellow text.

Style:
    `BRIGHT_YELLOW + BOLD`: codes 93 and 1 (`\\033[93;1m`).

Example:
    print(WARNING("disk is almost full"))
    # Writes the message in bold bright yellow.

Note:
    Equal to `BRIGHT_YELLOW_BOLD`; the name says what it is for.
"""
