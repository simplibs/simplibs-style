from .raise_styles_override_used_as_bool_error import raise_styles_override_used_as_bool_error


_DESIGN_NOTES = """
# Style Settings Class Validations Sub-Package

## Purpose
Diagnostic raisers for validating the use of style override managers.

## Internal Components Registry

| Component                                  | Type     | Description                                                    |
| :----------------------------------------- | :------- | :------------------------------------------------------------- |
| `raise_styles_override_used_as_bool_error` | Function | Raises `ParamError` when a `with` manager is used as a yes/no value. |
"""