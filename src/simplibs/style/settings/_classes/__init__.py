from .StylesOverride import StylesOverride
from .StylesSwitch import StylesSwitch


_DESIGN_NOTES = """
# Style Settings Internal Classes Sub-Package

## Purpose
Classes implementing the process-wide styles switch and scoped style overrides.

## Internal Components Registry

| Component        | Type        | Description                                                          |
| :--------------- | :---------- | :------------------------------------------------------------------- |
| `StylesOverride` | Class       | The `with` manager and decorator behind `styles_disabled` and `styles_enabled`; refuses to be used as a yes/no value. |
| `StylesSwitch`   | Class       | A mutable holder of one `bool`.                                      |
| `constants`      | Sub-package | Defines the scoped override state used by `StylesOverride`.          |
| `validations`    | Sub-package | Diagnostic raiser for using an override manager as a yes/no value.   |
"""