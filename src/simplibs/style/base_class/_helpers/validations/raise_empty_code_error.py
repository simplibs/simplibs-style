from typing import NoReturn
from simplibs.exception import ParamError


def raise_empty_code_error(
    code: str,
) -> NoReturn:
    """Raise ParamError when a style code has nothing in it.

    Args:
        code: The rejected code, as the caller wrote it.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="STYLE_EMPTY_CODE",
        label="style code",
        value=code,
        problem="The code has no digits in it.",
        expected="A code such as '91', '91m' or '\\033[91m'.",
        how_to_fix="Put the number of the code in front of the 'm' or the closing bracket.",
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_empty_code_error — A Code Without a Number

## Purpose
Covers `""`, blank text, `"m"` and `"\\033[m"`. The last two look valid and
are even a real sequence (the reset), but a style made of nothing but a
reset has no use, so they are refused with the same card as an empty string.
"""
