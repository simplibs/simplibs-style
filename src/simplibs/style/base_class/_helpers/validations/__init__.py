from .raise_code_not_text_error import raise_code_not_text_error
from .raise_empty_code_error import raise_empty_code_error
from .raise_invalid_ansi_format_error import raise_invalid_ansi_format_error
from .raise_invalid_code_error import raise_invalid_code_error


_DESIGN_NOTES = """
# Style Base Class Internal Helper Validations Sub-Package

## Purpose
Diagnostic raisers supporting internal style code normalization and validation.

## Internal Components Registry

| Component                         | Type     | Description                                                     |
| :-------------------------------- | :------- | :-------------------------------------------------------------- |
| `raise_code_not_text_error`       | Function | Raises `ParamError` when a code is not a string.                |
| `raise_empty_code_error`          | Function | Raises `ParamError` when a code has nothing in it.              |
| `raise_invalid_ansi_format_error` | Function | Raises `ParamError` for an escape sequence that does not end with `m`. |
| `raise_invalid_code_error`        | Function | Raises `ParamError` when a code is not digits joined by semicolons. |
"""