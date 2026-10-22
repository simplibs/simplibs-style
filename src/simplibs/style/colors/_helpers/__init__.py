from .choose_color_introducer import choose_color_introducer
from .parse_hex_color import parse_hex_color
from .require_color_value import require_color_value


_DESIGN_NOTES = """
# Style Colors Internal Helpers Sub-Package

## Purpose
Building blocks private to `colors/` for hex parsing, color value validation,
and foreground/background selection.

## Internal Components Registry

| Component                 | Type        | Description                                                       |
| :------------------------ | :---------- | :---------------------------------------------------------------- |
| `choose_color_introducer` | Function    | `38` for text, `48` for background — and checks the flag.         |
| `parse_hex_color`         | Function    | A hex string as `(r, g, b)`, or `None` when it is not one.        |
| `require_color_value`     | Function    | Requires an integer from 0 to 255, or raises.                     |
| `patterns`                | Sub-package | Defines the pattern used to recognize hexadecimal color values.  |
| `validations`             | Sub-package | Diagnostic raisers for invalid color values and background flags. |
"""