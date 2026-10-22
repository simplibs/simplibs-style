# Inners
from ._is_dumb_terminal import _is_dumb_terminal
from ._is_env_flag_set import _is_env_flag_set
from ._is_stdout_terminal import _is_stdout_terminal


def should_enable_styles_by_default() -> bool:
    """Decide from the environment whether styles should be on.

    Order of the decision: `NO_COLOR`, then `FORCE_COLOR`, then `TERM=dumb`,
    then whether standard output is a terminal.

    Returns:
        True when styles should be applied by default.
    """

    # 1. NO_COLOR is the user's explicit refusal — it beats everything
    if _is_env_flag_set("NO_COLOR"):
        return False

    # 2. FORCE_COLOR is the explicit request (CI logs that render colors)
    if _is_env_flag_set("FORCE_COLOR"):
        return True

    # 3. A terminal that cannot show escape codes
    if _is_dumb_terminal():
        return False

    # 4. Otherwise only a real terminal gets styles; pipes and files do not
    return _is_stdout_terminal()


_DESIGN_NOTES = """
# should_enable_styles_by_default — What the Environment Asks For

## Purpose
The starting position of the process-wide switch, and the answer of
`reset_styles_enabled`.

## The Order
Same order as in CPython's own colored output: `NO_COLOR` first (a
user-level refusal), `FORCE_COLOR` second, then `TERM=dumb`, and last
the terminal check. See no-color.org and force-color.org.

## Pipes and Files Stay Plain
Redirecting output into a file or a pipe, or capturing it in a test, gives
plain text, so no escape codes end up in the file. `FORCE_COLOR` overrides
that, for example for CI logs that render colors.

## Computed When Asked
Nothing is cached here; `GLOBAL_STYLES_SWITCH` calls it once at import and
`reset_styles_enabled` calls it again on demand.
"""
