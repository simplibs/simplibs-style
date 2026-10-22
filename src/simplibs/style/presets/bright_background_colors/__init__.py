from .BG_BRIGHT_BLACK import BG_BRIGHT_BLACK
from .BG_BRIGHT_RED import BG_BRIGHT_RED
from .BG_BRIGHT_GREEN import BG_BRIGHT_GREEN
from .BG_BRIGHT_YELLOW import BG_BRIGHT_YELLOW
from .BG_BRIGHT_BLUE import BG_BRIGHT_BLUE
from .BG_BRIGHT_MAGENTA import BG_BRIGHT_MAGENTA
from .BG_BRIGHT_CYAN import BG_BRIGHT_CYAN
from .BG_BRIGHT_WHITE import BG_BRIGHT_WHITE


_DESIGN_NOTES = """
# Bright Background Color Presets Sub-Package

## Purpose
The eight bright (high-intensity) background colors.

## One Preset, One File
Every preset has its own file and a full docstring, so hovering over the
name in an editor shows what it does, which code it writes and an example.
That is the reason for the small files; they carry no design notes of their
own, because a one-line definition has no decision worth recording.

## Internal Components Registry

| Component           | Type   | Description |
| :------------------ | :----- | :---------- |
| `BG_BRIGHT_BLACK`   | Preset | Bright black background. |
| `BG_BRIGHT_RED`     | Preset | Bright red background. |
| `BG_BRIGHT_GREEN`   | Preset | Bright green background. |
| `BG_BRIGHT_YELLOW`  | Preset | Bright yellow background. |
| `BG_BRIGHT_BLUE`    | Preset | Bright blue background. |
| `BG_BRIGHT_MAGENTA` | Preset | Bright magenta background. |
| `BG_BRIGHT_CYAN`    | Preset | Bright cyan background. |
| `BG_BRIGHT_WHITE`   | Preset | Bright white background. |
"""
