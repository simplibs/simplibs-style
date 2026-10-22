from .color_256 import color_256
from .color_hex import color_hex
from .color_rgb import color_rgb


_DESIGN_NOTES = """
# Style Colors Sub-Package

## Purpose
Builders of colors that have no preset: a color from the 256-color palette,
from three RGB channels, or from a hex string such as `"#ff8800"`. Each
returns a `StyleDefiner`, so the result combines with `+` and is called
like any preset.

## Internal Components Registry

| Component      | Type        | Description                                                  |
| :------------- | :---------- | :----------------------------------------------------------- |
| `color_256`    | Function    | A color from the 256-color palette (`0`-`255`).              |
| `color_hex`    | Function    | A true color from `"#rrggbb"` or `"#rgb"`.                   |
| `color_rgb`    | Function    | A true color from three channels (`0`-`255` each).           |
| `_helpers`     | Sub-package | Hex parsing, value check and the foreground/background pick. |
| `_validations` | Sub-package | Diagnostic raisers for a wrong value, hex or `background`.   |
"""
