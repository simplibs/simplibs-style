import sys


def _is_stdout_terminal() -> bool:
    """Check whether standard output is an interactive terminal.

    Returns:
        True when `sys.stdout` exists and reports itself as a terminal;
        False for a pipe, a file, a captured stream or a closed stream.
    """

    # 1. Without a stream (for example a windowed application) there is no terminal
    stream = sys.stdout
    if stream is None:
        return False

    # 2. Ask the stream; odd or closed streams are not terminals
    try:
        return bool(stream.isatty())
    except (AttributeError, ValueError, OSError):
        return False


_DESIGN_NOTES = """
# is_stdout_terminal — Escape Codes Only for Eyes

## Purpose
Text sent into a pipe or a file should not carry `\\033[91m`: the next
program or the next reader sees the codes as garbage.

## Standard Output Only
Styled text may also go to standard error. The default follows standard
output, the usual case; a program that styles only its error stream can
call `set_styles_enabled(True)` or use `styles_enabled()`.

## Never Raises
Captured streams (as in pytest) and closed streams answer `False` instead
of raising, so importing the library never fails because of its output.
"""
