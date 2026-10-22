from .DEBUG import DEBUG
from .INFO import INFO
from .SUCCESS import SUCCESS
from .WARNING import WARNING
from .ERROR import ERROR
from .CRITICAL import CRITICAL


_DESIGN_NOTES = """
# Log Level Presets Sub-Package

## Purpose
Styles named after what a message means, not after how it looks: `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR` and `CRITICAL`.

## One Preset, One File
Every preset has its own file and a full docstring, so hovering over the
name in an editor shows what it does, which code it writes and an example.
That is the reason for the small files; they carry no design notes of their
own, because a one-line definition has no decision worth recording.

## Named for the Meaning
A program that styles its output with `ERROR` can change what an error looks like
in one place. The names match the levels of the standard `logging` module,
plus `SUCCESS`.

## Internal Components Registry

| Component  | Type   | Description |
| :--------- | :----- | :---------- |
| `DEBUG`    | Preset | Style for debug messages: dimmed text. |
| `INFO`     | Preset | Style for informational messages: bright blue text. |
| `SUCCESS`  | Preset | Style for success messages: bold bright green text. |
| `WARNING`  | Preset | Style for warnings: bold bright yellow text. |
| `ERROR`    | Preset | Style for errors: bold bright red text. |
| `CRITICAL` | Preset | Style for critical failures: bold bright white text on red. |
"""
