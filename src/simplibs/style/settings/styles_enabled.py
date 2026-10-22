# Inners
from ._classes import StylesOverride


def styles_enabled() -> StylesOverride:
    """Enable styling for the duration of a `with` block or a decorated function.

    Forces styles on even when the output is not a terminal or `NO_COLOR`
    is set. The change holds for the current thread or async task only, and
    the previous state is restored when the block ends, even after an
    exception.

    Returns:
        A manager for a `with` statement. It is not a yes/no value: using it
        in a condition raises `ParamError` (ask `get_styles_enabled()` instead).

    Example:
        with styles_enabled():
            text = RED("always carries the escape codes")
    """

    # 1. A manager that forces styling on inside its block
    return StylesOverride(True)


_DESIGN_NOTES = """
# styles_enabled — Styled Text for One Block

## Purpose
The counterpart of `styles_disabled`. Tests of styled output run with
captured, non-terminal output, where styling is off by default; wrapping
them in this block makes the expected escape codes appear without touching
the process-wide switch.

## Stronger Than the Environment
It overrides `NO_COLOR` as well. A block that asks for styling explicitly
means it, and the caller who wrote the block is the one who decides.

## Call It, Do Not Ask It
Despite the name it is not a getter: `get_styles_enabled()` answers the
question. The manager refuses to be used as a condition (see
`StylesOverride`).
"""
