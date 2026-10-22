# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


WHITE = StyleDefiner(ANSI.FG_WHITE)
"""White text.

Style:
    Text color 37 (`\\033[37m`).

Example:
    print(WHITE("Something happened"))
    # Writes the text in white.

Note:
    Hard to read on a light background. For a stronger white use `BRIGHT_WHITE`.
"""
