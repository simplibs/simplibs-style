from .BG_BLACK import BG_BLACK
from .BG_RED import BG_RED
from .BG_GREEN import BG_GREEN
from .BG_YELLOW import BG_YELLOW
from .BG_BLUE import BG_BLUE
from .BG_MAGENTA import BG_MAGENTA
from .BG_CYAN import BG_CYAN
from .BG_WHITE import BG_WHITE


_DESIGN_NOTES = """
# Background Color Presets Sub-Package

## Purpose
The eight standard background colors.

## One Preset, One File
Every preset has its own file and a full docstring, so hovering over the
name in an editor shows what it does, which code it writes and an example.
That is the reason for the small files; they carry no design notes of their
own, because a one-line definition has no decision worth recording.

## Internal Components Registry

| Component    | Type   | Description |
| :----------- | :----- | :---------- |
| `BG_BLACK`   | Preset | Black background. |
| `BG_RED`     | Preset | Red background. |
| `BG_GREEN`   | Preset | Green background. |
| `BG_YELLOW`  | Preset | Yellow background. |
| `BG_BLUE`    | Preset | Blue background. |
| `BG_MAGENTA` | Preset | Magenta background. |
| `BG_CYAN`    | Preset | Cyan background. |
| `BG_WHITE`   | Preset | White background. |
"""
