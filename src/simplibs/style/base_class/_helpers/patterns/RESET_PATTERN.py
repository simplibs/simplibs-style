import re
from typing import Final
# Outers
from ....constants import ESCAPE_PREFIX, ESCAPE_SUFFIX


RESET_PATTERN: Final[re.Pattern[str]] = re.compile(
    f"{re.escape(ESCAPE_PREFIX)}0*{re.escape(ESCAPE_SUFFIX)}"
)
"""Any spelling of the lone reset sequence: `\\033[0m`, `\\033[00m` and `\\033[m`.

A reset combined with other codes (`\\033[0;1m`) does not match.
"""


_DESIGN_NOTES = """
# RESET_PATTERN — Every Way to Write "Switch All Styles Off"

## Purpose
Terminals accept three spellings of the same reset. This library writes
`\\033[0m`, but text that comes from elsewhere may hold the others, and
`apply_style` must recognize all of them to keep an outer style alive.

## Built From the Constants
The pattern is assembled from `ESCAPE_PREFIX` and `ESCAPE_SUFFIX` with
`0*` between them, so the frame of a sequence still has one definition.

## Lone Resets Only
`\\033[0;1m` resets and then sets bold in one sequence. What the outer style
should become after it is not knowable, so it is not matched.
"""
