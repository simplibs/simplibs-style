from .get_styles_enabled import get_styles_enabled
from .reset_styles_enabled import reset_styles_enabled
from .set_styles_enabled import set_styles_enabled
from .styles_disabled import styles_disabled
from .styles_enabled import styles_enabled


_DESIGN_NOTES = """
# Style Settings Sub-Package

## Purpose
Decides whether a style is applied or the text passes through unchanged.
Two layers work together:

* a **process-wide switch** — one position for the whole program, every
  thread included. `set_styles_enabled` moves it, `reset_styles_enabled`
  puts it back to what the environment says.
* a **scoped override** — `styles_disabled()` and `styles_enabled()` change
  the answer for the `with` block only, in the current thread or async task,
  and restore the previous answer afterwards, however the block ends.

An active override always wins over the process-wide switch.

## Internal Components Registry

| Component              | Type             | Description                                                            |
| :--------------------- | :--------------- | :--------------------------------------------------------------------- |
| `get_styles_enabled`   | Function         | The current answer: override first, then the process-wide switch.      |
| `set_styles_enabled`   | Function         | Moves the process-wide switch.                                         |
| `reset_styles_enabled` | Function         | Sets the process-wide switch back to the environment's default.        |
| `styles_disabled`      | Context manager  | Plain text inside the block.                                           |
| `styles_enabled`       | Context manager  | Styled text inside the block, even when the output is not a terminal.  |
| `_classes`             | Sub-package      | Classes implementing the process-wide switch and scoped override.      |
| `_constants`           | Sub-package      | The process-wide switch instance.                                      |
| `_helpers`             | Sub-package      | Environment and terminal checks used to determine the default.         |
| `_validations`         | Sub-package      | Diagnostic raiser for an invalid styles-enabled switch value.          |
"""
