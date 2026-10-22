from .STYLES_OVERRIDE import STYLES_OVERRIDE


_DESIGN_NOTES = """
# Style Settings Class Constants Sub-Package

## Purpose
Constants supporting the scoped style override mechanism.

## Internal Components Registry

| Component         | Type     | Description                                                   |
| :---------------- | :------- | :------------------------------------------------------------ |
| `STYLES_OVERRIDE` | Constant | The `ContextVar` holding the scoped override (`None` = no override). |
"""