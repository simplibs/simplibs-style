# Inners
from ._constants import GLOBAL_STYLES_SWITCH
from ._classes.constants import STYLES_OVERRIDE


def get_styles_enabled() -> bool:
    """Return whether styling is currently enabled.

    Returns:
        The scoped override when one is active (`styles_disabled()` or
        `styles_enabled()`), otherwise the process-wide switch.
    """

    # 1. A scoped override wins over everything else
    override = STYLES_OVERRIDE.get()
    if override is not None:
        return override

    # 2. Otherwise the process-wide switch decides
    return GLOBAL_STYLES_SWITCH.enabled


_DESIGN_NOTES = """
# get_styles_enabled — The One Question Every Style Asks

## Purpose
`StyleDefiner.__call__` asks it for every piece of text it styles, unless
the caller forces the answer with `use_style=`. It is two lookups and a
comparison, because it runs on every print.

## Override First
The block of a `with styles_disabled():` must stay plain even when the
process-wide switch says otherwise, so the scoped answer is read first.
"""
