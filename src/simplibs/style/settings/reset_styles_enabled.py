# Inners
from ._constants import GLOBAL_STYLES_SWITCH
from ._helpers import should_enable_styles_by_default


def reset_styles_enabled() -> None:
    """Set the process-wide switch back to what the environment says.

    The environment is read again: `NO_COLOR`, `FORCE_COLOR`, `TERM` and
    whether the output is a terminal.
    """

    # 1. Ask the environment again and store the answer
    GLOBAL_STYLES_SWITCH.enabled = should_enable_styles_by_default()


_DESIGN_NOTES = """
# reset_styles_enabled — Back to the Starting Position

## Purpose
Undoes every `set_styles_enabled`. Mostly for tests, which must not leak a
setting into the next test, and for programs that changed the environment
after the import.

## Reads the Environment Again
The starting position is computed once at import. A reset computes it anew,
so a changed `NO_COLOR` or a redirected output is noticed.
"""
