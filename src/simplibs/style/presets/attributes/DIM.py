# Outers
from ...constants import ANSI
from ...base_class import StyleDefiner


DIM = StyleDefiner(ANSI.DIM)
"""Dim (decreased intensity) text.

Style:
    Attribute 2 (`\\033[2m`).

Example:
    print(DIM("Less important"))
    # Writes "Less important" in a fainter shade.

Note:
    Not every terminal supports it. The `DEBUG` preset is built from it.
"""
