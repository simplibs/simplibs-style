# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


STRIKETHROUGH = StyleDefiner(ANSI.STRIKETHROUGH)
"""Text with a line through it.

Style:
    Attribute 9 (`\\033[9m`).

Example:
    print(STRIKETHROUGH("Done"))
    # Writes "Done" struck through.

Note:
    Not supported by every terminal.
"""
