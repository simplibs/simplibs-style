from .raise_color_background_not_bool_error import raise_color_background_not_bool_error
from .raise_color_not_int_error import raise_color_not_int_error
from .raise_color_out_of_range_error import raise_color_out_of_range_error


_DESIGN_NOTES = """
# Style Colors Internal Helper Validations Sub-Package

## Purpose
Diagnostic raisers supporting color value and background configuration validation.

## Internal Components Registry

| Component                               | Type     | Description                                            |
| :-------------------------------------- | :------- | :----------------------------------------------------- |
| `raise_color_background_not_bool_error` | Function | Raises `ParamError` when `background` is not a `bool`. |
| `raise_color_not_int_error`             | Function | Raises `ParamError` when a color value is not an integer. |
| `raise_color_out_of_range_error`        | Function | Raises `ParamError` when a color value is outside 0-255. |
"""