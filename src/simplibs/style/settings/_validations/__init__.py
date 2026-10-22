from .raise_styles_enabled_not_bool_error import raise_styles_enabled_not_bool_error


_DESIGN_NOTES = """
# Style Settings Validations Sub-Package

## Purpose
Diagnostic raisers for validating the process-wide styles-enabled switch.

## Internal Components Registry

| Component                             | Type     | Description                                                        |
| :------------------------------------ | :------- | :----------------------------------------------------------------- |
| `raise_styles_enabled_not_bool_error` | Function | Raises `ParamError` when the switch is given something other than a `bool`. |
"""