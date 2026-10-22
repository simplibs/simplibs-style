from typing import NoReturn
from simplibs.exception import ParamError


def raise_no_codes_error() -> NoReturn:
    """Raise ParamError when a style is created without any code."""

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="STYLE_NO_CODES",
        label="style codes",
        problem="A style needs at least one code.",
        expected="At least one code or another StyleDefiner.",
        how_to_fix=(
            "Pass a code such as '91', or a ready style such as RED.",
            "Use a preset like BOLD when you do not need a custom style.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_no_codes_error — A Style That Styles Nothing

## Purpose
`StyleDefiner()` would write `\\033[m`, which is the reset sequence. A style
that silently resets everything is the opposite of what anyone meant by
creating one.
"""
