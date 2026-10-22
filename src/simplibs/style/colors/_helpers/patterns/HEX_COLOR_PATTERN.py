import re
from typing import Final


HEX_COLOR_PATTERN: Final[re.Pattern[str]] = re.compile(r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})")
"""Shape of a hex color: an optional `#` and then 6 or 3 hex digits.

Group 1 holds the digits without the `#`. Use `fullmatch`, so nothing may
surround the color.
"""


_DESIGN_NOTES = """
# HEX_COLOR_PATTERN — What a Hex Color Looks Like

## Purpose
One definition of a hex color for `parse_hex_color`.

## Explicit Digits
`[0-9a-fA-F]` is written out, so only ASCII hex digits match.

## No Trailing Newline
`fullmatch` does not accept a trailing `"\\n"` the way `$` does, so
`"ff8800\\n"` from a file read is refused instead of passing quietly.
"""
