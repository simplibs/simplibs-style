from typing import NoReturn
from simplibs.exception import ParamError


def raise_invalid_code_error(
    code: str,
) -> NoReturn:
    """Raise ParamError when a style code is not digits joined by semicolons.

    Args:
        code: The rejected code, as the caller wrote it.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="STYLE_INVALID_CODE",
        label="style code",
        value=code,
        problem=(
            "The code contains something other than the digits 0-9 and single semicolons.",
            "Spaces, letters, signs and doubled or trailing semicolons are not allowed.",
        ),
        expected="Digits joined by semicolons, e.g. '91' or '38;5;208'.",
        how_to_fix=(
            "Remove everything but the digits and the separating semicolons.",
            "Use `color_256` or `color_rgb` to build the multi-part color codes.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_invalid_code_error — Digits and Semicolons, Nothing Else

## Purpose
The terminal does not complain about a bad code; it prints the rest of the
sequence as visible text or ignores it. The mistake would surface as strange
characters on the screen, far from the line that created the style.
"""
