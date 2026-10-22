from typing import Final
# Outers
from .._classes import StylesSwitch
from .._helpers import should_enable_styles_by_default


GLOBAL_STYLES_SWITCH: Final[StylesSwitch] = StylesSwitch(should_enable_styles_by_default())
"""The process-wide styling position, set from the environment at import."""


_DESIGN_NOTES = """
# GLOBAL_STYLES_SWITCH — The Starting Position

## Purpose
The single instance behind `get_styles_enabled` and `set_styles_enabled`.
It starts where the environment says (`NO_COLOR`, `FORCE_COLOR`, `TERM`,
terminal or not) and is moved only by `set_styles_enabled` and
`reset_styles_enabled`.
"""
