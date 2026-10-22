from typing import Final


ESCAPE_SUFFIX: Final[str] = "m"
"""End of every ANSI style sequence (SGR — Select Graphic Rendition)."""


_DESIGN_NOTES = """
# ESCAPE_SUFFIX — How a Style Sequence Ends

## Purpose
The `m` that closes a sequence like `\\033[91m`. Other final letters exist in
ANSI (cursor movement, screen clearing), but this library writes styles only,
so `m` is the only suffix it builds or accepts.
"""
