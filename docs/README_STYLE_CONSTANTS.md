# 🔢 `style/constants` — The Fixed Numbers of ANSI

The `constants` package names every fixed number and string of the ANSI standard **once**, so that
no other file in `simplibs-style` contains a bare `"\033["` or a magic `"91"`. The presets, the
color builders and `StyleDefiner` are all built from these names.

It holds four things: the table of SGR codes (`ANSI`) and the three constants that frame a
sequence (`ESCAPE_PREFIX`, `ESCAPE_SUFFIX`, `RESET_SEQUENCE`).

```python
from simplibs.style.constants import ANSI, ESCAPE_PREFIX, ESCAPE_SUFFIX, RESET_SEQUENCE
from simplibs.style import StyleDefiner

STYLE = StyleDefiner(ANSI.FG_RED, ANSI.UNDERLINE)      # the names instead of "31" and "4"

STYLE.sequence                                         # -> '\x1b[31;4m'
```

## A note on where they live

Unlike everything else, the constants are **not** exported from the root of the package — they are
reference data, not part of the everyday interface. Import them from the sub-package:

```python
from simplibs.style.constants import ANSI
```

Most programs never need them: a preset (`RED`) or a color builder (`color_hex(...)`) does the
same job with a friendlier name. The constants are for the moment you need a code that has **no
preset** — `BLINK_FAST`, the `*_OFF` codes, `FG_DEFAULT` — or want to build a style from the names
the standard gives.

## A note on what a sequence is

An ANSI style sequence has three parts, and each has exactly one definition in this package:

```
\033[   91;1   m
  │      │     └── ESCAPE_SUFFIX     the end of every style sequence
  │      └──────── the codes          joined by ";" — values from the ANSI table
  └─────────────── ESCAPE_PREFIX     the start of every style sequence
```

---

## 🧭 Table of Contents

* [`ESCAPE_PREFIX`](#escape_prefix)
* [`ESCAPE_SUFFIX`](#escape_suffix)
* [`RESET_SEQUENCE`](#reset_sequence)
* [`ANSI`](#ansi)
  * [Reset and text attributes](#reset-and-text-attributes)
  * [Attribute off](#attribute-off)
  * [Standard colors](#standard-colors)
  * [Bright colors](#bright-colors)
  * [Extended colors](#extended-colors)
* [Where the constants are used](#where-the-constants-are-used)

[⬅️ Back to main README](../README.md#-constants--the-fixed-numbers-of-ansi)

---

### `ESCAPE_PREFIX`

The start of every ANSI style sequence: the escape character followed by `[`.

**Type:**
* `Final[str]`: `"\033["`

**Example usage:**
```python
ESCAPE_PREFIX                          # -> '\x1b['
f"{ESCAPE_PREFIX}91{ESCAPE_SUFFIX}"    # -> '\x1b[91m'
```

`\033` is the escape character written in **octal** — the form the ANSI documentation uses, so the
code can be compared with the standard at a glance.

[▲ Back to top](#-table-of-contents)

---

### `ESCAPE_SUFFIX`

The end of every ANSI style sequence (SGR — *Select Graphic Rendition*).

**Type:**
* `Final[str]`: `"m"`

**Example usage:**
```python
ESCAPE_SUFFIX                          # -> 'm'
```

Other final letters exist in ANSI (cursor movement, screen clearing), but this library writes
**styles** only, so `m` is the only suffix it builds or accepts. This is why
[`StyleDefiner("\033[2J")`](README_STYLE_CLASS.md#styledefinercodes) is refused: that sequence
clears the screen, it is not a style.

[▲ Back to top](#-table-of-contents)

---

### `RESET_SEQUENCE`

The complete sequence that switches **every** style off.

**Type:**
* `Final[str]`: `"\033[0m"`

**Example usage:**
```python
RESET_SEQUENCE                         # -> '\x1b[0m'
f"{RED.sequence}text{RESET_SEQUENCE}"  # -> '\x1b[31mtext\x1b[0m'
```

Every styled text ends with it, so the style does not leak into whatever the terminal prints next.

**Under the hood:**
```python
RESET_SEQUENCE: Final[str] = f"{ESCAPE_PREFIX}{RESET}{ESCAPE_SUFFIX}"
```

It is **built** from its three named parts instead of being typed as `"\033[0m"`, so the prefix, the
code and the suffix each have exactly one definition.

[▲ Back to top](#-table-of-contents)

---

### `ANSI`

The table of SGR codes: every standard code under the name the standard gives it. It is a **module**
used as a namespace — `ANSI.BOLD`, `ANSI.FG_RED`, `ANSI.BG_BRIGHT_BLUE` — so a name always reads
`ANSI.…` and never collides with a preset of the same look (`ANSI.FG_RED` against `RED`).

**Type of every value:**
* `str`: A code is stored as the **text** it will become (`"31"`, not `31`), because codes are
  joined with `;` into one sequence.

**Example usage:**
```python
ANSI.BOLD                              # -> '1'
ANSI.FG_BRIGHT_RED                     # -> '91'
ANSI.BOLD_OFF                          # -> '22'

StyleDefiner(ANSI.FG_RED, ANSI.BOLD)   # -> StyleDefiner('31', '1')
```

**The table is complete, not only what is used.** Codes without a preset (`BLINK_FAST`, the
`*_OFF` codes, `FG_DEFAULT`) stay in it: it is reference data, and a missing row is more surprising
than an unused one. The sections below list **all 56** codes. The *Preset* column shows which
ones the library already turns into a ready-made style.

**Under the hood** *(the file is a plain list of assignments)*:
```python
# === RESET ===
RESET = "0"

# === TEXT ATTRIBUTES (1-9) ===
BOLD = "1"
DIM = "2"
...
```

> 💡 This is the one place that breaks "one constant per file". The codes are a single table copied
> from a standard, and splitting fifty-six one-line values into fifty-six files would hide the
> table instead of showing it.

#### Reset and text attributes

| Constant          | Code | Preset          | Meaning                                              |
|-------------------|------|-----------------|------------------------------------------------------|
| `RESET`           | `0`  | —               | Switches every style off (see `RESET_SEQUENCE`).     |
| `BOLD`            | `1`  | `BOLD`          | Bold (increased intensity).                          |
| `DIM`             | `2`  | `DIM`           | Dim (decreased intensity).                           |
| `ITALIC`          | `3`  | `ITALIC`        | Italics.                                             |
| `UNDERLINE`       | `4`  | `UNDERLINE`     | Underlined text.                                     |
| `BLINK`           | `5`  | `BLINK`         | Slowly blinking text.                                |
| `BLINK_FAST`      | `6`  | —               | Rapidly blinking text — rarely supported.            |
| `REVERSE`         | `7`  | `REVERSE`       | Text and background colors swapped.                  |
| `HIDDEN`          | `8`  | `HIDDEN`        | Concealed text.                                      |
| `STRIKETHROUGH`   | `9`  | `STRIKETHROUGH` | Text with a line through it.                         |

#### Attribute off

Switch off **one** attribute and leave the rest as it is — the finer tool next to `RESET`, which
switches off everything.

| Constant            | Code | Switches off                                                  |
|---------------------|------|---------------------------------------------------------------|
| `BOLD_OFF`          | `22` | Bold — normal intensity.                                      |
| `DIM_OFF`           | `22` | Dim — normal intensity.                                       |
| `ITALIC_OFF`        | `23` | Italics.                                                      |
| `UNDERLINE_OFF`     | `24` | Underline.                                                    |
| `BLINK_OFF`         | `25` | Blinking.                                                     |
| `REVERSE_OFF`       | `27` | Reversed colors.                                              |
| `HIDDEN_OFF`        | `28` | Concealed text.                                               |
| `STRIKETHROUGH_OFF` | `29` | Strikethrough.                                                |

> 💡 **Bold and dim share one "off" code.** `22` means *normal intensity* for both, so `BOLD_OFF`
> and `DIM_OFF` are the same value. `21` is **not** "bold off": many terminals read it as a double
> underline, which is why the table does not contain it.

#### Standard colors

| Constant     | Code | | Constant     | Code |
|--------------|------|-|--------------|------|
| `FG_BLACK`   | `30` | | `BG_BLACK`   | `40` |
| `FG_RED`     | `31` | | `BG_RED`     | `41` |
| `FG_GREEN`   | `32` | | `BG_GREEN`   | `42` |
| `FG_YELLOW`  | `33` | | `BG_YELLOW`  | `43` |
| `FG_BLUE`    | `34` | | `BG_BLUE`    | `44` |
| `FG_MAGENTA` | `35` | | `BG_MAGENTA` | `45` |
| `FG_CYAN`    | `36` | | `BG_CYAN`    | `46` |
| `FG_WHITE`   | `37` | | `BG_WHITE`   | `47` |
| `FG_DEFAULT` | `39` | | `BG_DEFAULT` | `49` |

`FG` colors the **text**, `BG` the **background**. The eight colors have presets (`RED`,
`BG_RED`, …); `FG_DEFAULT` and `BG_DEFAULT` do not — they put the text or background back to the
terminal's own color, leaving every other attribute as it is.

#### Bright colors

| Constant            | Code  | | Constant            | Code  |
|---------------------|-------|-|---------------------|-------|
| `FG_BRIGHT_BLACK`   | `90`  | | `BG_BRIGHT_BLACK`   | `100` |
| `FG_BRIGHT_RED`     | `91`  | | `BG_BRIGHT_RED`     | `101` |
| `FG_BRIGHT_GREEN`   | `92`  | | `BG_BRIGHT_GREEN`   | `102` |
| `FG_BRIGHT_YELLOW`  | `93`  | | `BG_BRIGHT_YELLOW`  | `103` |
| `FG_BRIGHT_BLUE`    | `94`  | | `BG_BRIGHT_BLUE`    | `104` |
| `FG_BRIGHT_MAGENTA` | `95`  | | `BG_BRIGHT_MAGENTA` | `105` |
| `FG_BRIGHT_CYAN`    | `96`  | | `BG_BRIGHT_CYAN`    | `106` |
| `FG_BRIGHT_WHITE`   | `97`  | | `BG_BRIGHT_WHITE`   | `107` |

All sixteen have a preset (`BRIGHT_RED`, `BG_BRIGHT_RED`, …).

#### Extended colors

These four are not colors by themselves: they **introduce** a color that is given by further
numbers. The [color builders](README_STYLE_COLORS.md) write them.

| Constant       | Code | Meaning                                                                      |
|----------------|------|------------------------------------------------------------------------------|
| `FG_EXTENDED`  | `38` | A **text** color follows.                                                    |
| `BG_EXTENDED`  | `48` | A **background** color follows.                                              |
| `EXTENDED_256` | `5`  | The color is one entry of the 256-color palette: `38;5;N`.                   |
| `EXTENDED_RGB` | `2`  | The color is true color: `38;2;R;G;B`.                                       |

**Example usage:**
```python
f"{ANSI.FG_EXTENDED};{ANSI.EXTENDED_256};208"          # -> '38;5;208'
f"{ANSI.BG_EXTENDED};{ANSI.EXTENDED_RGB};255;136;0"    # -> '48;2;255;136;0'
```

That is exactly what `color_256(208)` and `color_rgb(255, 136, 0, background=True)` write.

[▲ Back to top](#-table-of-contents)

---

### Where the constants are used

Nothing else in the library contains an escape character or a magic number.

| Constant         | Used by                                                                                          |
|------------------|--------------------------------------------------------------------------------------------------|
| `ESCAPE_PREFIX`  | `StyleDefiner` (builds the sequence), `normalize_code` (takes a given sequence apart), `RESET_PATTERN`, `apply_style` |
| `ESCAPE_SUFFIX`  | `StyleDefiner`, `normalize_code`, `RESET_PATTERN`                                                |
| `RESET_SEQUENCE` | `apply_style` — the end of every styled text                                                     |
| `ANSI.…`         | the [presets](README_STYLE_PRESETS.md) and the [color builders](README_STYLE_COLORS.md)          |

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-constants--the-fixed-numbers-of-ansi)
