from typing import Final
# Inners
from .ANSI import RESET
from .ESCAPE_PREFIX import ESCAPE_PREFIX
from .ESCAPE_SUFFIX import ESCAPE_SUFFIX


RESET_SEQUENCE: Final[str] = f"{ESCAPE_PREFIX}{RESET}{ESCAPE_SUFFIX}"
"""The complete sequence that switches every style off (`\\033[0m`)."""


_DESIGN_NOTES = """
# RESET_SEQUENCE — Back to Plain Text

## Purpose
Every styled text ends with this sequence, so the style does not leak into
whatever the terminal prints next.

## Built, Not Typed
It is assembled from its three named parts instead of written as `"\\033[0m"`,
so the prefix, the code and the suffix each have exactly one definition.
"""
