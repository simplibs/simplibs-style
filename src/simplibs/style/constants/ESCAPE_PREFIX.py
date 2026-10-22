from typing import Final


ESCAPE_PREFIX: Final[str] = "\033["
"""Start of every ANSI style sequence: the escape character followed by `[`."""


_DESIGN_NOTES = """
# ESCAPE_PREFIX — How a Style Sequence Begins

## Purpose
One named place for `"\\033["`, used when a sequence is built
(`StyleDefiner`) and when a user-given sequence is taken apart
(`normalize_code`).

## Octal Escape
`\\033` is the escape character written in octal. It is the form the ANSI
documentation uses, so the code can be compared with the standard at a glance.
"""
