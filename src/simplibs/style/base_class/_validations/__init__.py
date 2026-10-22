from .raise_no_codes_error import raise_no_codes_error
from .raise_use_style_not_bool_error import raise_use_style_not_bool_error


_DESIGN_NOTES = """
# Style Base Class Validations Sub-Package

## Purpose
Diagnostic raisers for validating style definitions and their configuration.

## Internal Components Registry

| Component                        | Type     | Description                                                          |
| :------------------------------- | :------- | :------------------------------------------------------------------- |
| `raise_no_codes_error`           | Function | Raises `ParamError` when a style is created without any code.        |
| `raise_use_style_not_bool_error` | Function | Raises `ParamError` when `use_style` is neither `None` nor a `bool`. |
"""
