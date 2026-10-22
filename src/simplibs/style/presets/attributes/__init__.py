from .BOLD import BOLD
from .DIM import DIM
from .ITALIC import ITALIC
from .UNDERLINE import UNDERLINE
from .BLINK import BLINK
from .REVERSE import REVERSE
from .HIDDEN import HIDDEN
from .STRIKETHROUGH import STRIKETHROUGH


_DESIGN_NOTES = """
# Style Attribute Presets Sub-Package

## Purpose
Ready-made styles that change how text looks without changing its color: bold, dim, italic, underline, blink, reverse, hidden and strikethrough.

## One Preset, One File
Every preset has its own file and a full docstring, so hovering over the
name in an editor shows what it does, which code it writes and an example.
That is the reason for the small files; they carry no design notes of their
own, because a one-line definition has no decision worth recording.

## Internal Components Registry

| Component       | Type   | Description |
| :-------------- | :----- | :---------- |
| `BOLD`          | Preset | Bold (increased intensity) text. |
| `DIM`           | Preset | Dim (decreased intensity) text. |
| `ITALIC`        | Preset | Italic text. |
| `UNDERLINE`     | Preset | Underlined text. |
| `BLINK`         | Preset | Blinking text. |
| `REVERSE`       | Preset | Reversed colors: text and background swapped. |
| `HIDDEN`        | Preset | Hidden (concealed) text. |
| `STRIKETHROUGH` | Preset | Text with a line through it. |
"""
