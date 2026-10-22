from typing import Any
# Outers
from ..constants import ESCAPE_PREFIX, ESCAPE_SUFFIX
from ..settings import get_styles_enabled
# Inners
from ._helpers import apply_style, normalize_code
from ._validations import raise_no_codes_error, raise_use_style_not_bool_error


class StyleDefiner:
    """A reusable terminal text style built from one or more ANSI codes.

    Rule:
        f"\\033[{code};{code}m{text}\\033[0m" — applied when styling is enabled.

    Example:
        RED = StyleDefiner("91")
        BOLD = StyleDefiner("1")
        ERROR = RED + BOLD

        print(ERROR("Something went wrong"))

    Attributes:
        codes: The bare codes of the style, e.g. `("91", "1")`.
        sequence: The ready-to-write escape sequence, e.g. `"\\033[91;1m"`.
    """

    __slots__ = ("_codes", "_sequence")

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        *codes: "str | StyleDefiner",
    ) -> None:
        """Build a style from codes and/or other styles.

        Args:
            *codes: Each entry is a code as `"91"`, `"91m"` or `"\\033[91m"`,
                a multi-part code such as `"38;5;208"`, or another
                `StyleDefiner` whose codes are taken over.

        Raises:
            ParamError: If no code is given, or if a code is not a string,
                is empty, or does not have the shape of an ANSI code.
        """

        # 1. A style without any code would be the reset sequence in disguise
        if not codes:
            raise_no_codes_error()

        # 2. Collect the bare codes of every entry
        parts: list[str] = []
        for entry in codes:

            # 2.1 A ready style brings its own, already normalized codes
            if isinstance(entry, StyleDefiner):
                parts.extend(entry.codes)

            # 2.2 Anything else must normalize into a bare code (or raise)
            else:
                parts.append(normalize_code(entry))

        # 3. Store the codes and the ready-to-use sequence built from them
        self._codes = tuple(parts)
        self._sequence = f"{ESCAPE_PREFIX}{';'.join(parts)}{ESCAPE_SUFFIX}"

    # ----------------------------------------------------------------------
    # Read-only data
    # ----------------------------------------------------------------------
    @property
    def codes(self) -> tuple[str, ...]:
        """The bare codes of the style."""
        return self._codes

    @property
    def sequence(self) -> str:
        """The escape sequence that switches this style on."""
        return self._sequence

    # ----------------------------------------------------------------------
    # Style application
    # ----------------------------------------------------------------------
    def __call__(
        self,
        text: Any,
        *,
        use_style: bool | None = None,
    ) -> str:
        """Apply this style to `text`.

        Args:
            text: The text to style. Anything that is not a string is
                converted with `str()` first.
            use_style: Overrides the current setting for this call only.
                `None` (default) asks `get_styles_enabled()`; `True` and
                `False` force styling on or off.

        Returns:
            The styled string, or the text unchanged when styling is off.

        Raises:
            ParamError: If `use_style` is not `None` or a `bool`.
        """

        # 1. Resolve whether styling applies for this call
        if use_style is None:
            enabled = get_styles_enabled()
        elif isinstance(use_style, bool):
            enabled = use_style
        else:
            raise_use_style_not_bool_error(use_style)

        # 2. The result is always a string, styled or not
        text = str(text)

        # 3. Apply, or pass through unchanged
        return apply_style(self._sequence, text) if enabled else text

    # ----------------------------------------------------------------------
    # Composition
    # ----------------------------------------------------------------------
    def __add__(self, other: Any) -> "StyleDefiner":
        """Combine this style with another via `style1 + style2`."""
        if not isinstance(other, StyleDefiner):
            return NotImplemented
        return StyleDefiner(self, other)

    def __radd__(self, other: Any) -> "StyleDefiner":
        """Support `sum([...])`, which starts its accumulator at `0`."""
        if type(other) is int and other == 0:
            return self
        return NotImplemented

    # ----------------------------------------------------------------------
    # Identity
    # ----------------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        """Two styles are equal when they write the same escape sequence."""
        if not isinstance(other, StyleDefiner):
            return NotImplemented
        return self._sequence == other._sequence

    def __hash__(self) -> int:
        return hash(self._sequence)

    def __repr__(self) -> str:
        return f"StyleDefiner({', '.join(repr(code) for code in self._codes)})"


_DESIGN_NOTES = """
# StyleDefiner — A Style You Call Like a Function

## Purpose
`RED("text")` returns the text wrapped in the escape sequence of red, or the
plain text when styling is off. Styles combine with `+` (`RED + BOLD`) and
are defined once, as presets or as the caller's own constants.

---

## 1. Bare Codes Are Stored, the Sequence Is Built From Them
Combining two styles must join their bare codes. Taking the finished
sequence of one style as if it were a code would turn `RED + BOLD` into
`\\033[\\033[31m;\\033[1mm`. So `codes` holds bare codes, `sequence` is built
from them once, and combining only joins the codes.

## 2. Immutable
`codes` and `sequence` are read-only properties. A style used as a preset
is shared by every importer; changing it would change them all. Equality and
the hash follow the sequence, so a style can be a dictionary key or a set
member and `RED == StyleDefiner("31")` is true.

## 3. Equal Means the Same Sequence
`StyleDefiner("31;1")` and `RED + BOLD` write the same bytes, so they are
equal even though their `codes` differ in how they are split.

## 4. The Call Is the Hot Path
`__call__` runs on every printed line, so it does only what it must: one
lookup of the setting, one `isinstance` when `use_style` is given, one
`str()`. A wrong `use_style` such as `"no"` is refused because a non-empty
string is truthy and would turn styling on by accident.

## 5. The Result Is Always a `str`
`RED(404)` returns `"404"` styled, and with styling off it returns `"404"`
too, never the number itself, so the caller can rely on the type.

## 6. `sum([...])` Works
`sum` starts from the integer `0`, so `__radd__` accepts exactly that value
and nothing else. A `bool` is not accepted (`type(other) is int`).

## 7. `repr` Can Be Pasted Back
`StyleDefiner('31', '1')` reads as the code that creates it. The raw escape
sequence would print as an invisible mess in a log.
"""
