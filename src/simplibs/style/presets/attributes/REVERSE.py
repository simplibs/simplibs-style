# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


REVERSE = StyleDefiner(ANSI.REVERSE)
"""Reversed colors: text and background swapped.

Style:
    Attribute 7 (`\\033[7m`).

Example:
    print(REVERSE("Selected"))
    # Writes "Selected" with text and background colors swapped.

Note:
    Highlights a word with no color of its own, so it works on any theme.
"""
