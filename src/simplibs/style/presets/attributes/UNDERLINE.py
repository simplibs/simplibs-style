# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


UNDERLINE = StyleDefiner(ANSI.UNDERLINE)
"""Underlined text.

Style:
    Attribute 4 (`\\033[4m`).

Example:
    print(UNDERLINE("Title"))
    # Writes "Title" underlined.

Note:
    Combines with a color: `RED + UNDERLINE`.
"""
