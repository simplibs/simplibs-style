from .attributes import (
    BOLD,
    DIM,
    ITALIC,
    UNDERLINE,
    BLINK,
    REVERSE,
    HIDDEN,
    STRIKETHROUGH,
)
from .standard_colors import (
    BLACK,
    RED,
    GREEN,
    YELLOW,
    BLUE,
    MAGENTA,
    CYAN,
    WHITE,
    BLACK_BOLD,
    RED_BOLD,
    GREEN_BOLD,
    YELLOW_BOLD,
    BLUE_BOLD,
    MAGENTA_BOLD,
    CYAN_BOLD,
    WHITE_BOLD,
)
from .bright_colors import (
    BRIGHT_BLACK,
    BRIGHT_RED,
    BRIGHT_GREEN,
    BRIGHT_YELLOW,
    BRIGHT_BLUE,
    BRIGHT_MAGENTA,
    BRIGHT_CYAN,
    BRIGHT_WHITE,
    BRIGHT_BLACK_BOLD,
    BRIGHT_RED_BOLD,
    BRIGHT_GREEN_BOLD,
    BRIGHT_YELLOW_BOLD,
    BRIGHT_BLUE_BOLD,
    BRIGHT_MAGENTA_BOLD,
    BRIGHT_CYAN_BOLD,
    BRIGHT_WHITE_BOLD,
)
from .background_colors import (
    BG_BLACK,
    BG_RED,
    BG_GREEN,
    BG_YELLOW,
    BG_BLUE,
    BG_MAGENTA,
    BG_CYAN,
    BG_WHITE,
)
from .bright_background_colors import (
    BG_BRIGHT_BLACK,
    BG_BRIGHT_RED,
    BG_BRIGHT_GREEN,
    BG_BRIGHT_YELLOW,
    BG_BRIGHT_BLUE,
    BG_BRIGHT_MAGENTA,
    BG_BRIGHT_CYAN,
    BG_BRIGHT_WHITE,
)
from .levels import (
    DEBUG,
    INFO,
    SUCCESS,
    WARNING,
    ERROR,
    CRITICAL,
)

__all__ = [
    # attributes — how text looks
    "BOLD",
    "DIM",
    "ITALIC",
    "UNDERLINE",
    "BLINK",
    "REVERSE",
    "HIDDEN",
    "STRIKETHROUGH",
    # standard colors
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "BLACK_BOLD",
    "RED_BOLD",
    "GREEN_BOLD",
    "YELLOW_BOLD",
    "BLUE_BOLD",
    "MAGENTA_BOLD",
    "CYAN_BOLD",
    "WHITE_BOLD",
    # bright colors
    "BRIGHT_BLACK",
    "BRIGHT_RED",
    "BRIGHT_GREEN",
    "BRIGHT_YELLOW",
    "BRIGHT_BLUE",
    "BRIGHT_MAGENTA",
    "BRIGHT_CYAN",
    "BRIGHT_WHITE",
    "BRIGHT_BLACK_BOLD",
    "BRIGHT_RED_BOLD",
    "BRIGHT_GREEN_BOLD",
    "BRIGHT_YELLOW_BOLD",
    "BRIGHT_BLUE_BOLD",
    "BRIGHT_MAGENTA_BOLD",
    "BRIGHT_CYAN_BOLD",
    "BRIGHT_WHITE_BOLD",
    # backgrounds
    "BG_BLACK",
    "BG_RED",
    "BG_GREEN",
    "BG_YELLOW",
    "BG_BLUE",
    "BG_MAGENTA",
    "BG_CYAN",
    "BG_WHITE",
    # bright backgrounds
    "BG_BRIGHT_BLACK",
    "BG_BRIGHT_RED",
    "BG_BRIGHT_GREEN",
    "BG_BRIGHT_YELLOW",
    "BG_BRIGHT_BLUE",
    "BG_BRIGHT_MAGENTA",
    "BG_BRIGHT_CYAN",
    "BG_BRIGHT_WHITE",
    # log levels — named for meaning
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


_DESIGN_NOTES = """
# Style Presets Package

## Purpose
Ready-made `StyleDefiner` instances for everything people reach for most:
text attributes, the sixteen text colors, the sixteen backgrounds and the
log levels. All of them are used without parentheses and called like a
function: `print(RED("text"))`.

## What the Folders Hold

| Folder                     | What it holds                                              |
| :------------------------- | :--------------------------------------------------------- |
| `attributes`               | Bold, dim, italic, underline, blink, reverse, hidden, strikethrough. |
| `standard_colors`          | The eight standard text colors and their bold variants.    |
| `bright_colors`            | The eight bright text colors and their bold variants.      |
| `background_colors`        | The eight standard backgrounds (`BG_RED`...).              |
| `bright_background_colors` | The eight bright backgrounds (`BG_BRIGHT_RED`...).         |
| `levels`                   | `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`. |

## Layering
`attributes` is the leaf. `standard_colors` and `bright_colors` build their
bold variants from it, `background_colors` stands alone, and `levels` builds
on all of them. The folders are imported in that order.

## Combining
Presets combine with `+` like any style: `RED + UNDERLINE`,
`BG_BLUE + BRIGHT_WHITE`. A color that has no preset comes from `colors/`
(`color_256`, `color_rgb`, `color_hex`).

## `__all__`
Defined here, because this is a domain folder; the sub-packages below export
by plain imports.
"""
