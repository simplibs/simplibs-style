import re
from typing import Final


CODE_PATTERN: Final[re.Pattern[str]] = re.compile(r"[0-9]+(?:;[0-9]+)*")
"""Shape of a bare ANSI code: ASCII digits, optionally joined by single semicolons.

`91`, `1` and `38;5;208` match; an empty string, `;;`, `1;` and `9x` do not.
Use `fullmatch`, so nothing may surround the code.
"""


_DESIGN_NOTES = """
# CODE_PATTERN — What a Bare Code Looks Like

## Purpose
One definition of a valid code, used by `normalize_code`.

## ASCII Digits Only
`[0-9]` instead of `\\d`, because `str.isdigit()` and `\\d` accept digits of
other scripts and characters like `²`, and a terminal understands none of
them. A check with `isdigit()` would let `"²"` through.

## The Value Is Not Range-Checked
`999` is accepted: the terminal ignores codes it does not know, and the list
of known codes changes. The shape is what this library guards.

## Semicolons Only
The colon form of true color (`38:2::255:0:0`) is not supported; every
terminal that understands it also understands the semicolon form.
"""
