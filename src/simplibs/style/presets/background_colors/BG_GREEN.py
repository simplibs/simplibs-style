# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BG_GREEN = StyleDefiner(ANSI.BG_GREEN)
"""Green background.

Style:
    Background color 42 (`\\033[42m`).

Example:
    print(BG_GREEN("ALERT"))
    # Writes the text on a green background.

Note:
    Set a text color too, so the text stays readable: `BG_GREEN + BRIGHT_WHITE`.
"""
