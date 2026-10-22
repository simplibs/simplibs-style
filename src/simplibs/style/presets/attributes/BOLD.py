# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


BOLD = StyleDefiner(ANSI.BOLD)
"""Bold (increased intensity) text.

Style:
    Attribute 1 (`\\033[1m`).

Example:
    print(BOLD("Important"))
    # Writes "Important" in bold.

Note:
    Some terminals show bold as a brighter color instead of a heavier font.
"""
