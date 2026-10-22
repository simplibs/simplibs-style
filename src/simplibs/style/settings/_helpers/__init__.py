from .should_enable_styles_by_default import should_enable_styles_by_default


_DESIGN_NOTES = """
# Style Settings Internal Helpers Sub-Package

## Purpose
Determines whether styles should be enabled by default using environment
settings and terminal capabilities.

## Internal Components Registry

| Component                         | Type        | Description                                                          |
| :-------------------------------- | :---------- | :------------------------------------------------------------------- |
| `should_enable_styles_by_default` | Function    | The environment's answer to "should styles be on?".                  |
| `_is_dumb_terminal`               | Module      | Checks whether `TERM` indicates a terminal that cannot show escape codes. |
| `_is_env_flag_set`                | Module      | Checks whether an environment variable is present and not empty.     |
| `_is_stdout_terminal`             | Module      | Checks whether standard output is an interactive terminal.           |
"""