# Inners
from ._constants import GLOBAL_STYLES_SWITCH
from ._validations import raise_styles_enabled_not_bool_error


def set_styles_enabled(
    value: bool
) -> None:
    """Switch styling on or off for the whole process.

    Args:
        value: `True` to style text, `False` to pass it through unchanged.

    Raises:
        ParamError: If `value` is not a `bool`.
    """

    # 1. Only a real bool is a position of the switch
    if not isinstance(value, bool):
        raise_styles_enabled_not_bool_error(value)

    # 2. Move the process-wide switch
    GLOBAL_STYLES_SWITCH.enabled = value


_DESIGN_NOTES = """
# set_styles_enabled — The Process-Wide Switch

## Purpose
One call at the start of a program (for example from a `--no-color` option)
that holds for every thread and every part of the program.

## Why Process-Wide, Not Per Context
A new thread starts with an empty context, so a setting stored in a
`ContextVar` and made in the main thread would silently not reach it. The
switch lives in one shared holder; only the temporary `with` overrides are
per thread or task.

## A Scoped Override Still Wins
Called inside `with styles_disabled():`, this changes the switch but the
block stays plain until it ends. That is the point of an override.

## A Strict Bool
`set_styles_enabled(1)` or `set_styles_enabled("no")` would be stored and
then read as truthy. Refusing them keeps a typo from looking like a setting.
"""
