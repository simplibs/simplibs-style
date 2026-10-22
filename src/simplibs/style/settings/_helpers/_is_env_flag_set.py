import os


def _is_env_flag_set(
    name: str
) -> bool:
    """Check whether an environment variable is present and not empty.

    Args:
        name: The name of the environment variable.

    Returns:
        True when the variable exists and holds more than whitespace.
    """

    # 1. Read the variable; a missing one is not set
    value = os.environ.get(name)
    if value is None:
        return False

    # 2. An empty or blank value counts as not set
    return value.strip() != ""


_DESIGN_NOTES = """
# is_env_flag_set — "Present and Not Empty"

## Purpose
`NO_COLOR` and `FORCE_COLOR` are both defined as "when present and not an
empty string". One definition of that phrase, used for both.

## The Value Is Not Interpreted
`NO_COLOR=0` still means "no color": the convention looks at presence, not
at what is written after the `=`.
"""
