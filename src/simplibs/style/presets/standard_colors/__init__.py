from .BLACK import BLACK
from .RED import RED
from .GREEN import GREEN
from .YELLOW import YELLOW
from .BLUE import BLUE
from .MAGENTA import MAGENTA
from .CYAN import CYAN
from .WHITE import WHITE
from .BLACK_BOLD import BLACK_BOLD
from .RED_BOLD import RED_BOLD
from .GREEN_BOLD import GREEN_BOLD
from .YELLOW_BOLD import YELLOW_BOLD
from .BLUE_BOLD import BLUE_BOLD
from .MAGENTA_BOLD import MAGENTA_BOLD
from .CYAN_BOLD import CYAN_BOLD
from .WHITE_BOLD import WHITE_BOLD


_DESIGN_NOTES = """
# Standard Color Presets Sub-Package

## Purpose
The eight standard text colors and their bold variants.

## One Preset, One File
Every preset has its own file and a full docstring, so hovering over the
name in an editor shows what it does, which code it writes and an example.
That is the reason for the small files; they carry no design notes of their
own, because a one-line definition has no decision worth recording.

## Themes Decide the Shade
Standard colors are remapped by the terminal theme, so the same preset looks
different on different setups. The bright colors are a sibling package.

## Internal Components Registry

| Component      | Type   | Description |
| :------------- | :----- | :---------- |
| `BLACK`        | Preset | Black text. |
| `RED`          | Preset | Red text. |
| `GREEN`        | Preset | Green text. |
| `YELLOW`       | Preset | Yellow text. |
| `BLUE`         | Preset | Blue text. |
| `MAGENTA`      | Preset | Magenta text. |
| `CYAN`         | Preset | Cyan text. |
| `WHITE`        | Preset | White text. |
| `BLACK_BOLD`   | Preset | Bold black text. |
| `RED_BOLD`     | Preset | Bold red text. |
| `GREEN_BOLD`   | Preset | Bold green text. |
| `YELLOW_BOLD`  | Preset | Bold yellow text. |
| `BLUE_BOLD`    | Preset | Bold blue text. |
| `MAGENTA_BOLD` | Preset | Bold magenta text. |
| `CYAN_BOLD`    | Preset | Bold cyan text. |
| `WHITE_BOLD`   | Preset | Bold white text. |
"""
