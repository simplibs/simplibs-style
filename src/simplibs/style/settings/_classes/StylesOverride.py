from contextlib import ContextDecorator
from contextvars import Token
# Inners
from .constants import STYLES_OVERRIDE
from .validations import raise_styles_override_used_as_bool_error


class StylesOverride(ContextDecorator):
    """A `with` block (or a decorator) that overrides the styling answer.

    Created by `styles_disabled()` and `styles_enabled()`. Inside the block
    `get_styles_enabled()` answers with the given value, for the current
    thread or async task only. The previous state is restored when the block
    ends, even after an exception.

    Raises:
        ParamError: If it is used as a yes/no value (`bool(...)`, `if ...:`).
    """

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        value: bool,
    ) -> None:

        # 1. Remember the answer to give, and prepare the stack of undo tokens
        self._value = value
        self._tokens: list[Token[bool | None]] = []

    # ----------------------------------------------------------------------
    # Decorator support
    # ----------------------------------------------------------------------
    def _recreate_cm(self) -> "StylesOverride":
        """Give every call of a decorated function its own manager."""
        return StylesOverride(self._value)

    # ----------------------------------------------------------------------
    # The with-block protocol
    # ----------------------------------------------------------------------
    def __enter__(self) -> None:

        # 1. Set the override and keep the token that undoes it
        self._tokens.append(STYLES_OVERRIDE.set(self._value))

    def __exit__(self, *exc_info: object) -> None:

        # 1. Restore the previous state, however the block ended
        STYLES_OVERRIDE.reset(self._tokens.pop())

    # ----------------------------------------------------------------------
    # Misuse guard
    # ----------------------------------------------------------------------
    def __bool__(self) -> bool:

        # 1. A block manager is not a yes/no answer — refuse loudly
        raise_styles_override_used_as_bool_error()

    def __repr__(self) -> str:
        return f"StylesOverride({self._value!r})"


_DESIGN_NOTES = """
# StylesOverride — A Block That Refuses to Be a Question

## Purpose
The manager behind `styles_disabled()` and `styles_enabled()`. It sets the
scoped override on entry and restores the previous state on exit.

## Why a Class and Not `@contextmanager`
Any object is true by default, so `if styles_enabled():` would always pass
and quietly do the wrong thing, a name that reads like a question being
an answer to none. `__bool__` makes that mistake fail at once, with a card
that points to `get_styles_enabled()`.

## Usable as a Decorator
`ContextDecorator` lets `@styles_disabled()` wrap a function. Every call of
the decorated function gets a fresh manager (`_recreate_cm`), so threads and
recursion never share one stack of tokens. Only plain functions are wrapped;
an `async def` needs a `with` block inside it.

## A Stack of Tokens
Entering the same manager twice (`with m: with m:`) is safe: each entry keeps
its own token and each exit undoes the latest one.
"""
