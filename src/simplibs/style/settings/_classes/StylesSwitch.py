class StylesSwitch:
    """A mutable holder of the process-wide styling position.

    Attributes:
        enabled: `True` when styles are applied, `False` when text passes
            through unchanged.
    """

    __slots__ = ("enabled",)

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, enabled: bool) -> None:

        # 1. Store the starting position
        self.enabled = enabled

    def __repr__(self) -> str:
        return f"StylesSwitch(enabled={self.enabled!r})"


_DESIGN_NOTES = """
# StylesSwitch — A Bool That Can Be Changed From Anywhere

## Purpose
A module-level `bool` cannot be reassigned from another module: after
`from x import SWITCH`, each importer holds its own copy. A holder object
is shared by identity, so `set_styles_enabled` changes what
`get_styles_enabled` reads, in every thread.

## Not a Lock
Assigning one attribute is a single step in Python, and the switch holds
one independent value, so nothing needs guarding.
"""
