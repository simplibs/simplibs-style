from .apply_style import apply_style
from .normalize_code import normalize_code


_DESIGN_NOTES = """
# Style Base Class Internal Helpers Sub-Package

## Purpose
Building blocks private to `base_class/` for style application, code normalization,
and their supporting patterns and validations.

## Internal Components Registry

| Component        | Type        | Description                                                              |
| :--------------- | :---------- | :----------------------------------------------------------------------- |
| `apply_style`    | Function    | Wraps a text in a sequence and keeps the style alive after inner resets. |
| `normalize_code` | Function    | Turns `"91"`, `"91m"` or `"\\\\033[91m"` into the bare code `"91"`.      |
| `patterns`       | Sub-package | Defines the code and reset patterns used by the internal style logic.    |
| `validations`    | Sub-package | Diagnostic raisers for invalid style codes and ANSI formats.             |
"""