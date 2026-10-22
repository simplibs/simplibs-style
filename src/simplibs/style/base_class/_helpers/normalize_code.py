from typing import Any
# Outers
from ...constants import ESCAPE_PREFIX, ESCAPE_SUFFIX
# Inners
from .patterns import CODE_PATTERN
from .validations import (
    raise_code_not_text_error,
    raise_empty_code_error,
    raise_invalid_ansi_format_error,
    raise_invalid_code_error,
)


def normalize_code(
    code: Any,
) -> str:
    """Normalize a single ANSI code fragment into its bare form.

    Accepts three input shapes and returns the same normalized form for
    all of them:
        "91"          -> "91"
        "91m"         -> "91"
        "\\033[91m"   -> "91"

    Args:
        code: The raw code to normalize.

    Returns:
        The bare code: digits, optionally joined by semicolons
        (e.g. `"91"` or `"38;5;208"`).

    Raises:
        ParamError: If `code` is not a string, is empty, is an escape
            sequence that does not end with `m`, or has any other shape than
            digits joined by semicolons.
    """

    # 1. Only a string can be a code
    if not isinstance(code, str):
        raise_code_not_text_error(code)

    # 2. Strip the frame: the full escape form, or the trailing "m" shorthand
    body = code
    if code.startswith(ESCAPE_PREFIX):
        if not code.endswith(ESCAPE_SUFFIX):
            raise_invalid_ansi_format_error(code)
        body = code[len(ESCAPE_PREFIX):-len(ESCAPE_SUFFIX)]
    elif code.endswith(ESCAPE_SUFFIX):
        body = code[:-len(ESCAPE_SUFFIX)]

    # 3. Nothing is left of the code: "", "   ", "m" or "\\033[m"
    if not body.strip():
        raise_empty_code_error(code)

    # 4. What is left must be digits joined by semicolons
    if CODE_PATTERN.fullmatch(body) is None:
        raise_invalid_code_error(code)

    # 5. Return the bare code
    return body


_DESIGN_NOTES = """
# normalize_code — One Code, One Shape

## Purpose
People write the same code three ways, and `StyleDefiner` accepts all of
them. This function reduces them to the bare form, so the sequence is built
from one shape only.

## Strict by Design
An empty body (`"m"`), `";;"`, digits of other scripts and a non-string such
as `91` each get a diagnostic card, instead of reaching the terminal as
garbage or failing deep inside with a bare `AttributeError`.

## Blank Counts as Empty
`"   "` and `"m"` are reported as empty, not as "invalid characters": the
person forgot the code, they did not write a wrong one.

## Not Exported
A helper of `base_class/`. If authors of their own styles need it, a `tools/`
facade can export it later, the way `simplibs-path` does.
"""
