import os


def _is_dumb_terminal() -> bool:
    """Check whether `TERM` declares a terminal without escape code support.

    Returns:
        True when `TERM` is `dumb` (case-insensitive).
    """

    # 1. A missing TERM is not "dumb" — it is simply unknown
    return os.environ.get("TERM", "").strip().lower() == "dumb"


_DESIGN_NOTES = """
# is_dumb_terminal — A Terminal That Prints Escape Codes Literally

## Purpose
Some editors and CI shells set `TERM=dumb` and show `\\033[91m` as text.
Styles are not applied there, even when the output looks interactive.
"""
