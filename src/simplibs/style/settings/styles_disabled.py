# Inners
from ._classes import StylesOverride


def styles_disabled() -> StylesOverride:
    """Disable styling for the duration of a `with` block or a decorated function.

    The change holds for the current thread or async task only, and the
    previous state is restored when the block ends, even after an exception.

    Returns:
        A manager for a `with` statement. It is not a yes/no value: using it
        in a condition raises `ParamError` (ask `get_styles_enabled()` instead).

    Example:
        with styles_disabled():
            print(RED("this prints as plain text"))

        @styles_disabled()
        def render_report() -> str:
            ...
    """

    # 1. A manager that forces styling off inside its block
    return StylesOverride(False)


_DESIGN_NOTES = """
# styles_disabled — Plain Text for One Block

## Purpose
For output that must contain no escape codes: text written to a file,
copied into a message or compared in a test.

## Call It, Do Not Ask It
The function returns a manager for a `with` statement. The question "are
styles on right now?" is `get_styles_enabled()`; the manager refuses to
answer it (see `StylesOverride`).
"""
