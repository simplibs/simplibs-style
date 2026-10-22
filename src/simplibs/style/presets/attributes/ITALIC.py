# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


ITALIC = StyleDefiner(ANSI.ITALIC)
"""Italic text.

Style:
    Attribute 3 (`\\033[3m`).

Example:
    print(ITALIC("Emphasis"))
    # Writes "Emphasis" in italics.

Note:
    Not shown by every terminal; some older ones show reverse video instead.
"""
