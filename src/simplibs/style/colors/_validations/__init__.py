from .raise_color_hex_invalid_error import raise_color_hex_invalid_error


_DESIGN_NOTES = """
# Style Colors Validations Sub-Package

## Purpose
Diagnostic raisers for invalid hex color values.

## Internal Components Registry

| Component                       | Type     | Description                                                |
| :------------------------------ | :------- | :--------------------------------------------------------- |
| `raise_color_hex_invalid_error` | Function | Raises `ParamError` when a value is not a hex color string. |
"""