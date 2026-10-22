from contextvars import ContextVar
from typing import Final


STYLES_OVERRIDE: Final[ContextVar[bool | None]] = ContextVar("STYLES_OVERRIDE", default=None)
"""The scoped override of styling: `True`, `False`, or `None` for "no override"."""


_DESIGN_NOTES = """
# STYLES_OVERRIDE — The Answer of the Current Block

## Purpose
Holds what `styles_disabled()` and `styles_enabled()` decided, separately
for every thread and every async task, so two tasks can print in different
modes at the same time.

## `None` Means "Ask the Switch"
Without an override the variable is `None`, and `get_styles_enabled` falls
through to the process-wide switch. A third state is needed because `False`
is a real answer, not an absence.
"""
