from typing import NoReturn
from simplibs.exception import ParamError


def raise_invalid_ansi_format_error(
    code: str,
) -> NoReturn:
    """Raise ParamError when an escape sequence does not end with 'm'.

    Args:
        code: The rejected code, as the caller wrote it.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="STYLE_INVALID_ANSI_FORMAT",
        label="style code",
        value=code,
        problem=(
            "The code starts like an ANSI escape sequence but does not end with 'm'.",
            "Only style sequences (ending with 'm') are supported.",
        ),
        expected="A complete sequence such as '\\033[91m', or a bare code such as '91'.",
        how_to_fix=(
            "Add the closing 'm' to the sequence.",
            "Or pass the bare number without the escape prefix.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_invalid_ansi_format_error — A Sequence That Is Not a Style

## Purpose
`\\033[2J` clears the screen and `\\033[10;5H` moves the cursor. They start
the same way as a style and end differently. Putting one into a style would
make every use of it clear the screen, so the library says no.
"""
