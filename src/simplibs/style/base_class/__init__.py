from .StyleDefiner import StyleDefiner


_DESIGN_NOTES = """
# Style Base Class Sub-Package

## Purpose
The one class of the library: `StyleDefiner`, a reusable terminal style
built from one or more ANSI codes. Everything else (presets, color builders)
only creates and combines instances of it.

## Internal Components Registry

| Component       | Type        | Description                                                       |
| :-------------- | :---------- | :---------------------------------------------------------------- |
| `StyleDefiner`  | Class       | An immutable style: combine with `+`, apply by calling.           |
| `_helpers`      | Sub-package | `normalize_code`, `apply_style` and the code pattern.             |
| `_validations`  | Sub-package | Diagnostic raisers for a wrong code and a wrong `use_style`.      |
"""
