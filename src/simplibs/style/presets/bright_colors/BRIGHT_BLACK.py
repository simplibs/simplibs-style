# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BRIGHT_BLACK = StyleDefiner(ANSI.FG_BRIGHT_BLACK)
"""Bright black text.

Style:
    Text color 90 (`\\033[90m`).

Example:
    print(BRIGHT_BLACK("Something happened"))
    # Writes the text in bright black.

Note:
    Usually renders as gray — a good choice for secondary text such as timestamps.
"""
