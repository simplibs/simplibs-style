from typing import NoReturn
from simplibs.exception import ParamError


def raise_styles_override_used_as_bool_error() -> NoReturn:
    """Raise ParamError when `styles_enabled()` or `styles_disabled()` is used as a condition."""

    # 1. Raise structured ParamError wrapping a TypeError
    raise ParamError(
        error_name="STYLE_OVERRIDE_USED_AS_BOOL",
        label="styles override",
        problem=(
            "`styles_enabled()` and `styles_disabled()` are blocks for a `with` statement, not yes/no questions.",
            "Used as a condition they would be always true.",
        ),
        expected="A `with` statement, e.g. `with styles_enabled():`.",
        how_to_fix=(
            "Use `get_styles_enabled()` to ask whether styles are on.",
            "Use `with styles_enabled():` to force styles on for a block.",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_styles_override_used_as_bool_error — A Name That Reads Like a Question

## Purpose
`if styles_enabled():` looks like a check and is not one. The mistake is
refused where it is made, instead of silently styling (or not styling) the
text for the rest of the program.
"""
