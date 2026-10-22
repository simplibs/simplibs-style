from . import ANSI
from .ESCAPE_PREFIX import ESCAPE_PREFIX
from .ESCAPE_SUFFIX import ESCAPE_SUFFIX
from .RESET_SEQUENCE import RESET_SEQUENCE


_DESIGN_NOTES = """
# Style Constants Sub-Package

## Purpose
The fixed numbers and strings of the ANSI standard, named once so that no
other file contains a bare `"\\033["` or a magic `"91"`.

## Internal Components Registry

| Component        | Type     | Description                                                          |
| :--------------- | :------- | :------------------------------------------------------------------- |
| `ANSI`           | Module   | The table of SGR codes (`ANSI.BOLD`, `ANSI.FG_RED`, `ANSI.BG_BLUE`...). |
| `ESCAPE_PREFIX`  | Constant | The start of every style sequence (`ESC` + `[`).                     |
| `ESCAPE_SUFFIX`  | Constant | The end of every style sequence (`m`).                               |
| `RESET_SEQUENCE` | Constant | The complete sequence that switches every style off.                 |
"""
