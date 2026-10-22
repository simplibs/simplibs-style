from .CODE_PATTERN import CODE_PATTERN
from .RESET_PATTERN import RESET_PATTERN


_DESIGN_NOTES = """
# Style Base Class Internal Constants Sub-Package

## Purpose
Constants defining the patterns used by the internal style logic.

## Internal Components Registry

| Component       | Type     | Description                                                        |
| :-------------- | :------- | :----------------------------------------------------------------- |
| `CODE_PATTERN`  | Constant | The shape of a bare code: digits, optionally joined by semicolons. |
| `RESET_PATTERN` | Constant | Any spelling of the lone reset sequence.                           |
"""