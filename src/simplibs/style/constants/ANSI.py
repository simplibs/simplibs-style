# === RESET ===
RESET = "0"

# === TEXT ATTRIBUTES (1-9) ===
BOLD = "1"
DIM = "2"
ITALIC = "3"
UNDERLINE = "4"
BLINK = "5"
BLINK_FAST = "6"
REVERSE = "7"
HIDDEN = "8"
STRIKETHROUGH = "9"

# === ATTRIBUTE OFF (21-29) ===
# Bold and dim share one "off" code: "22" means normal intensity for both.
# ("21" is NOT bold off — many terminals read it as double underline.)
BOLD_OFF = "22"
DIM_OFF = "22"
ITALIC_OFF = "23"
UNDERLINE_OFF = "24"
BLINK_OFF = "25"
REVERSE_OFF = "27"
HIDDEN_OFF = "28"
STRIKETHROUGH_OFF = "29"

# === FOREGROUND — STANDARD (30-37, 39) ===
FG_BLACK = "30"
FG_RED = "31"
FG_GREEN = "32"
FG_YELLOW = "33"
FG_BLUE = "34"
FG_MAGENTA = "35"
FG_CYAN = "36"
FG_WHITE = "37"
FG_DEFAULT = "39"

# === BACKGROUND — STANDARD (40-47, 49) ===
BG_BLACK = "40"
BG_RED = "41"
BG_GREEN = "42"
BG_YELLOW = "43"
BG_BLUE = "44"
BG_MAGENTA = "45"
BG_CYAN = "46"
BG_WHITE = "47"
BG_DEFAULT = "49"

# === FOREGROUND — BRIGHT (90-97) ===
FG_BRIGHT_BLACK = "90"
FG_BRIGHT_RED = "91"
FG_BRIGHT_GREEN = "92"
FG_BRIGHT_YELLOW = "93"
FG_BRIGHT_BLUE = "94"
FG_BRIGHT_MAGENTA = "95"
FG_BRIGHT_CYAN = "96"
FG_BRIGHT_WHITE = "97"

# === BACKGROUND — BRIGHT (100-107) ===
BG_BRIGHT_BLACK = "100"
BG_BRIGHT_RED = "101"
BG_BRIGHT_GREEN = "102"
BG_BRIGHT_YELLOW = "103"
BG_BRIGHT_BLUE = "104"
BG_BRIGHT_MAGENTA = "105"
BG_BRIGHT_CYAN = "106"
BG_BRIGHT_WHITE = "107"

# === EXTENDED COLORS (introduce 5;N or 2;R;G;B) ===
FG_EXTENDED = "38"
BG_EXTENDED = "48"
EXTENDED_256 = "5"
EXTENDED_RGB = "2"


_DESIGN_NOTES = """
# ANSI — The Table of SGR Codes

## Purpose
Every standard SGR (Select Graphic Rendition) code under the name the
standard gives it: `ANSI.BOLD`, `ANSI.FG_RED`, `ANSI.BG_BRIGHT_BLUE`. The
presets are built from these names, never from bare numbers.

## One File, On Purpose
This is the one place that breaks "one constant per file". The codes are a
single table copied from a standard, and splitting sixty one-line values
into sixty files would hide the table instead of showing it. Used as a
namespace (`from ..constants import ANSI`), so a name always reads
`ANSI.RED`-style and never collides with a preset such as `RED`.

## Strings, Not Integers
Codes are joined with `;` into one sequence, so they are kept as the text
they will become.

## Complete, Not Only What Is Used
Codes without a preset (`BLINK_FAST`, `HIDDEN`, the `*_OFF` codes) stay in
the table: it is reference data, and a missing row is more surprising than
an unused one.

## Extended Colors
`FG_EXTENDED` and `BG_EXTENDED` introduce a color given by further numbers;
`EXTENDED_256` (`5;N`) and `EXTENDED_RGB` (`2;R;G;B`) say which kind follows.
The color builders in `colors/` write them.
"""
