# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BLACK = StyleDefiner(ANSI.FG_BLACK)
"""Black text.

Style:
    Text color 30 (`\\033[30m`).

Example:
    print(BLACK("Something happened"))
    # Writes the text in black.

Note:
    Hard to read on a dark background. For gray text use `BRIGHT_BLACK`.
"""
