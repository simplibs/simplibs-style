# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BLINK = StyleDefiner(ANSI.BLINK)
"""Blinking text.

Style:
    Attribute 5 (`\\033[5m`).

Example:
    print(BLINK("Attention"))
    # Writes "Attention" blinking.

Note:
    Many terminals ignore blinking or let the user turn it off, and blinking text is tiring to read. Use it sparingly.
"""
