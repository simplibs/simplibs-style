# 🌈 `simplibs-style`

[![PyPI](https://img.shields.io/pypi/v/simplibs-style)](https://pypi.org/project/simplibs-style/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-style/blob/main/LICENSE)
[![tests](https://github.com/simplibs/simplibs-style/actions/workflows/tests.yml/badge.svg)](https://github.com/simplibs/simplibs-style/actions)

**Terminal styles as plain Python objects — defined once, applied safely.**

A lightweight Python library that replaces hand-written escape codes (`"\033[91;1m"`) with small,
named `StyleDefiner` objects. A style is **called like a function** to style a text, **combines
with the plain `+` operator**, and — when the output is not a terminal — quietly hands the text
back unchanged, so a log file or a pipe never fills up with `\033[0m`. Colors beyond the sixteen
basic ones come from three builders (256-color, RGB, hex), and sixty-two ready-made presets cover
the rest.

```python
from simplibs.style import RED, BOLD, BG_BLUE, BRIGHT_WHITE, ERROR, color_hex

print(RED("Plain red"))
print((BG_BLUE + BRIGHT_WHITE + BOLD)(" INFO "))       # styles combine with +
print(color_hex("#ff8800")("A brand orange"))          # any color, straight from a design
print(ERROR("could not open the file"))                # named for what it means
```

> Everything works without configuration: in a terminal the text is styled, in a pipe, a file or a
> test it stays plain. `NO_COLOR`, `FORCE_COLOR` and a dumb `TERM` are respected.

---

## 🧭 The Core Philosophy

Escape codes written by hand are strings that nobody can read: `"\033[38;5;208;1m"` says nothing
about what it does, a forgotten `\033[0m` bleeds one color into everything printed after it, and a
log written into a file ends up full of codes no editor can display. `simplibs-style` replaces the
string with a small immutable object that knows its own codes, resets itself and knows when to stay
quiet.

* **A style is an object, not a string.** `RED`, `ERROR` and `color_hex("#ff8800")` are all the
  same thing — a `StyleDefiner` — so everything you learn about one holds for all of them: call it,
  add it, compare it, use it as a dictionary key.
* **Composition is `+`.** `RED + BOLD`, `BG_BLUE + BRIGHT_WHITE + BOLD`, `sum([RED, UNDERLINE])`.
  A style never changes; combining two builds a new one.
* **Quiet when it should be.** A style is applied only when the output is an interactive terminal.
  A program can overrule it everywhere (`set_styles_enabled(False)` for a `--no-color` option), for
  one block (`with styles_disabled():`) or for one call (`RED("x", use_style=False)`).
* **Nesting just works.** A styled text inside another styled text keeps the outer style after the
  inner one ends — the inner reset never switches the outer color off.
* **Mistakes fail where they are made.** A code is checked for its shape, a number for its range,
  a hex color for its form, and a flag must be a real `bool` — `use_style="no"` would be truthy and
  style the text, so it is refused instead. Nothing ends up as strange characters on the screen,
  far from the line that caused it.
* **Names for meaning, not only for looks.** `ERROR`, `WARNING`, `SUCCESS` say what a message is;
  what an error looks like can be changed in one place.
* **Layers that only look left.**
  `constants` and `settings` ← `base_class` ← `colors` and `presets` — every layer imports only
  from those before it.

```python
ERROR = BRIGHT_RED + BOLD                       # a style is built from other styles
ERROR.codes                                     # -> ('91', '1')
ERROR.sequence                                  # -> '\x1b[91;1m'
RED("x", use_style="no")                        # -> raises: only True, False or None decide
```

---

## 📦 Installation

```bash
pip install simplibs-style
```

Requires Python 3.11+. The only runtime dependency (installed automatically) is the simplibs
`exception` library, which provides the structured error messages.

---

## 🚀 Quick Start in 60 Seconds

### Level 1: Presets — call them like functions

```python
from simplibs.style import RED, BOLD, UNDERLINE, BG_BLUE, BRIGHT_WHITE, ERROR, SUCCESS

print(RED("Plain red"))
print(UNDERLINE("A title"))
print((RED + UNDERLINE)("Combined with +"))
print((BG_BLUE + BRIGHT_WHITE + BOLD)(" INFO "))

print(SUCCESS("all tests passed"))               # styles named for the meaning
print(ERROR("could not open the file"))
```

Presets are used **without parentheses** and called like a function. There are sixty-two of them:
attributes, the sixteen text colors in two intensities, the sixteen backgrounds and six log levels.

### Level 2: Any color — 256, RGB or hex

```python
from simplibs.style import color_256, color_rgb, color_hex, BOLD

ORANGE = color_hex("#ff8800")                    # as copied from a design tool
print((ORANGE + BOLD)("A brand orange"))
print(color_256(24, background=True)(" deep blue "))
print(color_rgb(255, 136, 0)("The same orange, from three numbers"))

color_hex("#f80") == color_rgb(255, 136, 0)      # -> True
```

### Level 3: Decide when styles apply

```python
from simplibs.style import RED, set_styles_enabled, styles_disabled, styles_enabled

RED("Error")                                     # styled in a terminal, plain in a pipe or a file

with styles_disabled():                          # this block: always plain
    report = RED("goes into a file")             # -> 'goes into a file'

with styles_enabled():                           # this block: always styled — handy in a test
    assert RED("x") == "\033[31mx\033[0m"

RED("x", use_style=False)                        # one single call
set_styles_enabled(False)                        # the whole program, e.g. a --no-color option
```

### Level 4: Define your own

```python
from simplibs.style import StyleDefiner, UNDERLINE

PATH = StyleDefiner("38;5;110", UNDERLINE)       # codes and other styles, mixed freely
print(PATH("src/app.py"))

StyleDefiner("91")                               # a bare code
StyleDefiner("\033[91m")                         # or a whole sequence, as copied from a manual
```

---

## 🛠️ Architecture & Package Structure

```
src/simplibs/style/
├── constants/             ◄── The fixed numbers of ANSI (the table of SGR codes, ESCAPE_PREFIX,
│                              ESCAPE_SUFFIX, RESET_SEQUENCE)
├── settings/              ◄── Whether styles are applied (the switch, the scoped overrides,
│                              the start from the environment)
├── base_class/            ◄── StyleDefiner — the one class everything is built on
├── colors/                ◄── color_256, color_rgb, color_hex
└── presets/               ◄── Ready-made styles (attributes, standard_colors, bright_colors,
                               background_colors, bright_background_colors, levels)
```

The root of the package exports everything you normally use — `StyleDefiner`, the three color
builders, the five settings functions and all sixty-two presets (71 names in total). The constants
are reference data and are imported from their own folder:

```python
from simplibs.style import StyleDefiner, color_hex, styles_disabled, RED, BOLD, ERROR   # everyday use
from simplibs.style.constants import ANSI, ESCAPE_PREFIX, RESET_SEQUENCE                # reference data
```

---

## 🧩 The `StyleDefiner` Class

Every style in this library is a `StyleDefiner`: an immutable object holding one or more ANSI codes.
It does three things — holds the codes, applies them when called, and combines with other styles.

```python
class StyleDefiner:
    def __init__(self, *codes: str | StyleDefiner): ...      # "91", "91m", "\033[91m", "38;5;208", RED

    @property
    def codes(self) -> tuple[str, ...]: ...                  # ('91', '1')
    @property
    def sequence(self) -> str: ...                           # '\x1b[91;1m'

    def __call__(self, text, *, use_style: bool | None = None) -> str: ...
    def __add__(self, other: StyleDefiner) -> StyleDefiner: ...
```

➡️ Full method-by-method reference: [README_STYLE_CLASS](https://github.com/simplibs/simplibs-style/blob/main/docs/README_STYLE_CLASS.md)

### What the constructor accepts

| You write         | Stored as    | Note                                                       |
|-------------------|--------------|------------------------------------------------------------|
| `"91"`            | `"91"`       | The bare code.                                             |
| `"91m"`           | `"91"`       | With the closing `m`.                                      |
| `"\033[91m"`      | `"91"`       | The complete escape sequence.                              |
| `"38;5;208"`      | `"38;5;208"` | A multi-part code: digits joined by single semicolons.     |
| `RED`             | `"91"` …     | Another style; its codes are taken over.                   |

### What calling a style does

| `use_style` | Result                                                            |
|-------------|-------------------------------------------------------------------|
| `None`      | Follows the current setting — styled in a terminal, plain otherwise. |
| `True`      | Styled, whatever the setting says.                                |
| `False`     | Plain, whatever the setting says.                                 |
| anything else | `ParamError` — `"no"` would be truthy and style the text.       |

---

## 📖 Quick Reference

### 🚦 `settings/` — Whether styles are applied

Three layers work together: the argument `use_style=` (one call), the scoped override (one `with`
block, per thread or async task) and the process-wide switch (the whole program). The more specific
layer wins; the switch starts from the environment (`NO_COLOR` → `FORCE_COLOR` → `TERM=dumb` →
is the output a terminal?).

| Function / manager     | Description / Parameters                                                                   |
|------------------------|--------------------------------------------------------------------------------------------|
| `get_styles_enabled`   | Whether styles are on right now — the override when active, otherwise the switch.          |
| `set_styles_enabled`   | Moves the process-wide switch (`value: bool`).                                             |
| `reset_styles_enabled` | Puts the switch back to what the environment says.                                         |
| `styles_disabled`      | A `with` block (or decorator) in which the text is always plain.                           |
| `styles_enabled`       | A `with` block (or decorator) in which the text is always styled — even into a file.       |

➡️ [README_STYLE_SETTINGS](https://github.com/simplibs/simplibs-style/blob/main/docs/README_STYLE_SETTINGS.md)

---

### 🎨 `colors/` — Any color beyond the presets

All three return a `StyleDefiner` and take the same keyword-only `background` flag (`True` colors
the background instead of the text).

| Function     | Description / Parameters                                                                        |
|--------------|-------------------------------------------------------------------------------------------------|
| `color_256`  | One of 256 palette colors — code `38;5;N` / `48;5;N` (`n`, `background=False`).                |
| `color_rgb`  | A true-color value, three channels `0`–`255` — `38;2;R;G;B` (`r`, `g`, `b`, `background=False`).|
| `color_hex`  | The same, written as `"#ff8800"`, `"ff8800"`, `"#f80"` or `"f80"` (`value`, `background=False`).|

A terminal without true-color support shows the nearest color it has, or none.

➡️ [README_STYLE_COLORS](https://github.com/simplibs/simplibs-style/blob/main/docs/README_STYLE_COLORS.md)

---

### 🎁 `presets/` — Ready-made styles

Sixty-two `StyleDefiner` instances in six groups. Used without parentheses, combined with `+`.

| Group                      | Count | Presets                                                                       |
|----------------------------|-------|-------------------------------------------------------------------------------|
| **attributes**             | 8     | `BOLD`, `DIM`, `ITALIC`, `UNDERLINE`, `BLINK`, `REVERSE`, `HIDDEN`, `STRIKETHROUGH` |
| **standard_colors**        | 16    | `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE` and `…_BOLD` of each |
| **bright_colors**          | 16    | `BRIGHT_BLACK` … `BRIGHT_WHITE` and `BRIGHT_…_BOLD` of each                   |
| **background_colors**      | 8     | `BG_BLACK` … `BG_WHITE`                                                       |
| **bright_background_colors** | 8   | `BG_BRIGHT_BLACK` … `BG_BRIGHT_WHITE`                                         |
| **levels**                 | 6     | `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`                    |

The log levels are named after what a message **means**, so what an error looks like can change in
one place:

| Preset     | Looks like                              | Codes           |
|------------|-----------------------------------------|-----------------|
| `DEBUG`    | dimmed text (an alias of `DIM`)         | `2`             |
| `INFO`     | bright blue (an alias of `BRIGHT_BLUE`) | `94`            |
| `SUCCESS`  | bold bright green                       | `92`, `1`       |
| `WARNING`  | bold bright yellow                      | `93`, `1`       |
| `ERROR`    | bold bright red                         | `91`, `1`       |
| `CRITICAL` | bold bright white on a red background   | `41`, `97`, `1` |

➡️ [README_STYLE_PRESETS](https://github.com/simplibs/simplibs-style/blob/main/docs/README_STYLE_PRESETS.md)

---

### 🔢 `constants/` — The fixed numbers of ANSI

Reference data, imported from `simplibs.style.constants`. Most programs never need it: a preset or
a color builder does the same job with a friendlier name.

| Component        | Description                                                                                  |
|------------------|----------------------------------------------------------------------------------------------|
| `ANSI`           | The table of all 56 SGR codes under the names the standard gives (`ANSI.BOLD`, `ANSI.FG_RED`, `ANSI.BG_BRIGHT_BLUE`, `ANSI.BOLD_OFF` …) — a module used as a namespace. |
| `ESCAPE_PREFIX`  | The start of every style sequence: `"\033["`.                                                |
| `ESCAPE_SUFFIX`  | The end of every style sequence: `"m"`.                                                      |
| `RESET_SEQUENCE` | The complete sequence that switches every style off: `"\033[0m"`.                            |

➡️ [README_STYLE_CONSTANTS](https://github.com/simplibs/simplibs-style/blob/main/docs/README_STYLE_CONSTANTS.md)

---

## 🪟 Terminal Notes

The library writes the escape sequences; it does not configure the terminal. Where they differ, it
says so:

* **Where the decision is made:** the default follows the **standard output**. A program that styles
  only its error stream can force styles on with `set_styles_enabled(True)` or `styles_enabled()`.
* **`NO_COLOR` and `FORCE_COLOR`:** a variable counts when it exists and is not empty — its value is
  not interpreted, so `NO_COLOR=0` still means "no color". `NO_COLOR` beats `FORCE_COLOR`.
* **True color:** `color_rgb` and `color_hex` always write the true-color sequence. A terminal without
  support shows the nearest color it has. For output that must work everywhere, use `color_256` or
  a preset.
* **Bold:** some terminals show it as a brighter color instead of a heavier font, so `RED_BOLD` can
  look like `BRIGHT_RED`.
* **Terminal themes:** the sixteen basic colors are the user's own theme colors, so `BLACK` can be
  nearly invisible on a dark background. Colors from `color_256` (index 16 up), `color_rgb` and
  `color_hex` are fixed.
* **Older consoles:** a console that does not understand ANSI sequences cannot show the styles. Turn
  them off with `set_styles_enabled(False)`.

---

## ⚠️ Exceptions

Styles raise structured [`simplibs.exception`](https://pypi.org/project/simplibs-exception/) cards
at the moment of the mistake — never later as strange characters in the output. Every error is a
`ParamError`, every error name starts with `STYLE_`, and each is documented next to the function
that raises it.

| Error name                        | Wraps                      | Raised when                                                   |
|-----------------------------------|----------------------------|---------------------------------------------------------------|
| `STYLE_NO_CODES`                  | `ValueError`               | `StyleDefiner()` got no code at all.                          |
| `STYLE_CODE_NOT_TEXT`             | `TypeError`                | A code is neither a string nor a style (`StyleDefiner(91)`).  |
| `STYLE_EMPTY_CODE`                | `ValueError`               | A code has no digits (`""`, `"m"`, `"\033[m"`).               |
| `STYLE_INVALID_ANSI_FORMAT`       | `ValueError`               | An escape sequence that does not end with `m` (`"\033[2J"`).  |
| `STYLE_INVALID_CODE`              | `ValueError`               | Anything but digits joined by single semicolons (`"9x"`).     |
| `STYLE_USE_STYLE_NOT_BOOL`        | `TypeError`                | `use_style` is neither `None` nor a `bool`.                   |
| `STYLE_STYLES_ENABLED_NOT_BOOL`   | `TypeError`                | `set_styles_enabled` got something other than a `bool`.       |
| `STYLE_OVERRIDE_USED_AS_BOOL`     | `TypeError`                | `styles_enabled()` / `styles_disabled()` is used as a yes/no value (`if styles_enabled():`). |
| `STYLE_COLOR_NOT_INT`             | `TypeError`                | A color value is not an integer (`"208"`, `208.0`, `True`).   |
| `STYLE_COLOR_OUT_OF_RANGE`        | `ValueError`               | A color value is outside `0`–`255`.                           |
| `STYLE_COLOR_HEX_INVALID`         | `ValueError` / `TypeError` | Not a hex color: a wrong text, or a value that is not text.   |
| `STYLE_COLOR_BACKGROUND_NOT_BOOL` | `TypeError`                | `background` is not a `bool`.                                 |

Calling a style never raises for where the output goes: a captured stream, a closed stream or a
missing `sys.stdout` simply count as "not a terminal".

---

## 🔗 Related libraries

* **[`simplibs-exception`](https://pypi.org/project/simplibs-exception/)** — the structured exception cards behind every error here.

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:**
We actively minimize cognitive load. Code is atomized into small, self-contained units,
files are named directly after the logical task they perform, and explanations describe
*why* something is designed, not just *what* it is.
* **Programmer's Zen:**
Nothing should be missing, and nothing should be superfluous. We value clean execution
paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:**
We actively anticipate edge cases and failure modes so that only safe operational paths
remain. Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:**
Find the most direct path to the goal in as few operational steps as possible without
taking shortcuts on safety, readability, or completeness.
* **Code as Craft:**
Code should be pleasant to look at, readable at a glance, and evoke structural harmony.
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. We strongly believe in
community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
  or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---
