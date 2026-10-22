from .settings import (
    get_styles_enabled,
    reset_styles_enabled,
    set_styles_enabled,
    styles_disabled,
    styles_enabled,
)
from .base_class import StyleDefiner
from .colors import (
    color_256,
    color_hex,
    color_rgb,
)
from .presets import (
    BOLD,
    DIM,
    ITALIC,
    UNDERLINE,
    BLINK,
    REVERSE,
    HIDDEN,
    STRIKETHROUGH,
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
    BG_BLACK,
    BG_RED,
    BG_GREEN,
    BG_YELLOW,
    BG_BLUE,
    BG_MAGENTA,
    BG_CYAN,
    BG_WHITE,
    BG_BRIGHT_BLACK,
    BG_BRIGHT_RED,
    BG_BRIGHT_GREEN,
    BG_BRIGHT_YELLOW,
    BG_BRIGHT_BLUE,
    BG_BRIGHT_MAGENTA,
    BG_BRIGHT_CYAN,
    BG_BRIGHT_WHITE,
    DEBUG,
    INFO,
    SUCCESS,
    WARNING,
    ERROR,
    CRITICAL,
)

__all__ = [
    # base class — the style itself
    "StyleDefiner",
    # colors — styles built from numbers or hex
    "color_256",
    "color_rgb",
    "color_hex",
    # settings — whether styles are applied
    "get_styles_enabled",
    "set_styles_enabled",
    "reset_styles_enabled",
    "styles_disabled",
    "styles_enabled",
    # presets — attributes
    "BOLD",
    "DIM",
    "ITALIC",
    "UNDERLINE",
    "BLINK",
    "REVERSE",
    "HIDDEN",
    "STRIKETHROUGH",
    # presets — standard colors
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
    # presets — bright colors
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
    # presets — backgrounds
    "BG_BLACK",
    "BG_RED",
    "BG_GREEN",
    "BG_YELLOW",
    "BG_BLUE",
    "BG_MAGENTA",
    "BG_CYAN",
    "BG_WHITE",
    # presets — bright backgrounds
    "BG_BRIGHT_BLACK",
    "BG_BRIGHT_RED",
    "BG_BRIGHT_GREEN",
    "BG_BRIGHT_YELLOW",
    "BG_BRIGHT_BLUE",
    "BG_BRIGHT_MAGENTA",
    "BG_BRIGHT_CYAN",
    "BG_BRIGHT_WHITE",
    # presets — log levels
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


_DESIGN_NOTES = """
# simplibs-style — Package Root

## Purpose
Terminal text styles without escape codes in the caller's code:
`print(RED_BOLD("Something went wrong"))`. A style is an object, styles
combine with `+`, and one switch decides whether they are applied.

## What the Root Exports
Everything a caller needs, from one import line:

    from simplibs.style import RED, BOLD, color_hex, styles_disabled

* **`StyleDefiner`** — the one class; define a style of your own with it.
* **Color builders** — `color_256`, `color_rgb`, `color_hex`.
* **Settings** — `get_styles_enabled`, `set_styles_enabled`,
  `reset_styles_enabled` and the two blocks `styles_disabled()` and
  `styles_enabled()`.
* **Presets** — sixty-two ready-made styles: attributes, standard and bright
  colors with their bold variants, backgrounds and log levels.

## Why the Presets Are Exported Too
Unlike `rules/` and `actions/` in other libraries, presets are what most
callers come for, and `from simplibs.style import RED` is the shortest way
to say it. The names are distinct, uppercase and few enough to read in one
list. They stay importable from `simplibs.style.presets` as well.

## What the Root Deliberately Does NOT Export
* **`normalize_code`** — a helper of `base_class/`; a style is built from codes
  through `StyleDefiner`, which calls it.
* **The `ANSI` table and the escape constants** — they live in
  `simplibs.style.constants` for authors who need a code by its name.

## Dependencies
Only `simplibs-exception` (`ParamError`).

## `__all__`
Defined here and in `presets/`; the other sub-packages export by plain
imports.
"""
