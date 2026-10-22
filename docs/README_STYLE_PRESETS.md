# 🎁 `style/presets` — Ready-Made Styles

Sixty-two styles that are ready the moment you import them: text attributes, the sixteen text
colors in two intensities, the sixteen backgrounds and six styles named after what a message
*means*. Every one is a [`StyleDefiner`](README_STYLE_CLASS.md) — used **without parentheses**,
called like a function.

```python
from simplibs.style import RED, BOLD, BG_BLUE, BRIGHT_WHITE, ERROR

print(RED("Plain red"))
print((RED + BOLD)("Bold red"))                 # presets combine with +
print((BG_BLUE + BRIGHT_WHITE)(" Badge "))
print(ERROR("could not open the file"))         # named for the meaning
```

## A note on how they are made

A preset is nothing more than a `StyleDefiner` with a fixed code, written in one line:

```python
RED = StyleDefiner(ANSI.FG_RED)                 # code 31
RED_BOLD = RED + BOLD                           # codes 31 and 1
ERROR = BRIGHT_RED + BOLD                       # codes 91 and 1
```

Nothing special happens in them, so everything from [`StyleDefiner`](README_STYLE_CLASS.md) holds:
they are **immutable**, they **combine** with `+`, and they respect the
[settings](README_STYLE_SETTINGS.md) — in a pipe or a file they write plain text.

Each preset has its own small file with a full docstring, so hovering over the name in an editor
shows what it writes, which code it uses and an example.

## A note on what is *not* here

A preset exists where there is a name that everyone agrees on. A color that has no name — a
brand orange, a gray from a ramp — comes from the [color builders](README_STYLE_COLORS.md)
(`color_256`, `color_rgb`, `color_hex`) and combines with the presets the same way.

```python
BRAND = color_hex("#ff8800") + BOLD
```

---

## 🧭 Table of Contents

* [Attributes](#attributes)
* [Standard colors](#standard-colors)
* [Bright colors](#bright-colors)
* [Background colors](#background-colors)
* [Bright background colors](#bright-background-colors)
* [Log levels](#log-levels)
* [Combining presets](#combining-presets)
* [Quick reference — all sixty-two](#quick-reference--all-sixty-two)

[⬅️ Back to main README](../README.md#-presets--ready-made-styles)

---

### Attributes

How the text looks, not what color it is. Eight presets, each a single code.

| Preset          | Code | Writes                                      | Note                                                                    |
|-----------------|------|---------------------------------------------|-------------------------------------------------------------------------|
| `BOLD`          | `1`  | bold (increased intensity)                  | Some terminals show it as a brighter color instead of a heavier font.   |
| `DIM`           | `2`  | dim (decreased intensity)                   | Not every terminal supports it. `DEBUG` is built from it.               |
| `ITALIC`        | `3`  | italics                                     | Not shown by every terminal; some older ones show reverse video instead.|
| `UNDERLINE`     | `4`  | underlined text                             | Combines with a color: `RED + UNDERLINE`.                               |
| `BLINK`         | `5`  | blinking text                               | Many terminals ignore or disable it, and it is tiring to read. Use sparingly. |
| `REVERSE`       | `7`  | text and background colors swapped          | Highlights a word with no color of its own, so it works on any theme.   |
| `HIDDEN`        | `8`  | concealed text                              | Hidden on the screen **only** — it stays in the output and can be copied. Not a way to protect secrets. |
| `STRIKETHROUGH` | `9`  | text with a line through it                 | Not supported by every terminal.                                        |

**Example usage:**
```python
print(BOLD("Important"))
print(UNDERLINE("Title"))
print(REVERSE("Selected"))
```

**Under the hood:**
```python
BOLD = StyleDefiner(ANSI.BOLD)               # "1"
```

> 💡 `REVERSE` is the attribute to reach for when you need a highlight that must look right on
> **any** terminal theme: it swaps whatever the user's colors already are.

[▲ Back to top](#-table-of-contents)

---

### Standard colors

The eight standard text colors, and a bold variant of each. Sixteen presets.

| Preset     | Code | Bold variant   | Codes     |
|------------|------|----------------|-----------|
| `BLACK`    | `30` | `BLACK_BOLD`   | `30`, `1` |
| `RED`      | `31` | `RED_BOLD`     | `31`, `1` |
| `GREEN`    | `32` | `GREEN_BOLD`   | `32`, `1` |
| `YELLOW`   | `33` | `YELLOW_BOLD`  | `33`, `1` |
| `BLUE`     | `34` | `BLUE_BOLD`    | `34`, `1` |
| `MAGENTA`  | `35` | `MAGENTA_BOLD` | `35`, `1` |
| `CYAN`     | `36` | `CYAN_BOLD`    | `36`, `1` |
| `WHITE`    | `37` | `WHITE_BOLD`   | `37`, `1` |

**Example usage:**
```python
print(GREEN("Ready"))
print(RED_BOLD("Something happened"))
RED_BOLD.sequence                    # -> '\x1b[31;1m'
```

**Under the hood:**
```python
RED = StyleDefiner(ANSI.FG_RED)      # "31"
RED_BOLD = RED + BOLD                # "31", "1"
```

> 💡 The look of these eight colors belongs to the **user's terminal theme** — `BLACK` is nearly
> invisible on a dark background and `WHITE` on a light one. On many terminals bold also brightens
> the color, so `RED_BOLD` can look like `BRIGHT_RED`.

[▲ Back to top](#-table-of-contents)

---

### Bright colors

The eight bright (high-intensity) text colors, and a bold variant of each. Sixteen presets.

| Preset           | Code | Bold variant          | Codes     |
|------------------|------|-----------------------|-----------|
| `BRIGHT_BLACK`   | `90` | `BRIGHT_BLACK_BOLD`   | `90`, `1` |
| `BRIGHT_RED`     | `91` | `BRIGHT_RED_BOLD`     | `91`, `1` |
| `BRIGHT_GREEN`   | `92` | `BRIGHT_GREEN_BOLD`   | `92`, `1` |
| `BRIGHT_YELLOW`  | `93` | `BRIGHT_YELLOW_BOLD`  | `93`, `1` |
| `BRIGHT_BLUE`    | `94` | `BRIGHT_BLUE_BOLD`    | `94`, `1` |
| `BRIGHT_MAGENTA` | `95` | `BRIGHT_MAGENTA_BOLD` | `95`, `1` |
| `BRIGHT_CYAN`    | `96` | `BRIGHT_CYAN_BOLD`    | `96`, `1` |
| `BRIGHT_WHITE`   | `97` | `BRIGHT_WHITE_BOLD`   | `97`, `1` |

**Example usage:**
```python
print(BRIGHT_CYAN("Hint"))
print(BRIGHT_RED_BOLD("Failed"))
```

**Under the hood:**
```python
BRIGHT_RED = StyleDefiner(ANSI.FG_BRIGHT_RED)    # "91"
BRIGHT_RED_BOLD = BRIGHT_RED + BOLD              # "91", "1"
```

> 💡 `BRIGHT_BLACK` is the usual way to write a **gray** — a good fit for secondary text such as
> timestamps, paths or hints. Where `DIM` is not supported, it still works.

[▲ Back to top](#-table-of-contents)

---

### Background colors

The eight standard backgrounds. Text color is left as it is, so they are usually combined with a
text color. Eight presets.

| Preset       | Code  | | Preset       | Code  |
|--------------|-------|-|--------------|-------|
| `BG_BLACK`   | `40`  | | `BG_BLUE`    | `44`  |
| `BG_RED`     | `41`  | | `BG_MAGENTA` | `45`  |
| `BG_GREEN`   | `42`  | | `BG_CYAN`    | `46`  |
| `BG_YELLOW`  | `43`  | | `BG_WHITE`   | `47`  |

**Example usage:**
```python
print((BG_BLUE + BRIGHT_WHITE)(" INFO "))
print((BG_YELLOW + BLACK)(" NOTE "))
```

**Under the hood:**
```python
BG_RED = StyleDefiner(ANSI.BG_RED)      # "41"
```

> 💡 A background alone changes only the background, so the text keeps its own color. Always pick a
> text color that reads on it (`BG_YELLOW + BLACK`, `BG_BLUE + BRIGHT_WHITE`).

[▲ Back to top](#-table-of-contents)

---

### Bright background colors

The eight bright backgrounds. Eight presets.

| Preset              | Code  | | Preset                | Code  |
|---------------------|-------|-|-----------------------|-------|
| `BG_BRIGHT_BLACK`   | `100` | | `BG_BRIGHT_BLUE`      | `104` |
| `BG_BRIGHT_RED`     | `101` | | `BG_BRIGHT_MAGENTA`   | `105` |
| `BG_BRIGHT_GREEN`   | `102` | | `BG_BRIGHT_CYAN`      | `106` |
| `BG_BRIGHT_YELLOW`  | `103` | | `BG_BRIGHT_WHITE`     | `107` |

**Example usage:**
```python
print((BG_BRIGHT_GREEN + BLACK)(" OK "))
```

**Under the hood:**
```python
BG_BRIGHT_RED = StyleDefiner(ANSI.BG_BRIGHT_RED)    # "101"
```

[▲ Back to top](#-table-of-contents)

---

### Log levels

Styles named after what a message **means**, not after how it looks. The names match the levels of
the standard `logging` module, plus `SUCCESS`.

| Preset     | Looks like                         | Codes            | Same as                |
|------------|------------------------------------|------------------|------------------------|
| `DEBUG`    | dimmed text                        | `2`              | `DIM` *(the same object)* |
| `INFO`     | bright blue text                   | `94`             | `BRIGHT_BLUE` *(the same object)* |
| `SUCCESS`  | bold bright green text             | `92`, `1`        | equal to `BRIGHT_GREEN_BOLD` |
| `WARNING`  | bold bright yellow text            | `93`, `1`        | equal to `BRIGHT_YELLOW_BOLD` |
| `ERROR`    | bold bright red text               | `91`, `1`        | equal to `BRIGHT_RED_BOLD` |
| `CRITICAL` | bold bright white on a red background | `41`, `97`, `1` | — (a style of its own) |

**Example usage:**
```python
print(DEBUG("cache miss for key 42"))
print(INFO("server started on port 8000"))
print(SUCCESS("all tests passed"))
print(WARNING("disk is almost full"))
print(ERROR("could not open the file"))
print(CRITICAL("database is unreachable"))
```

**Why they exist.** A program that styles its output with `ERROR` can change what an error looks
like in **one place**, and the code that prints it keeps reading as what it means. `CRITICAL` has a
red *background* so that it stands out from `ERROR` even when the colors of the text are hard to
tell apart.

**Same look, different name.** The levels are built from the plain presets, so a level and its
look-alike write the same bytes:

```python
ERROR == BRIGHT_RED_BOLD        # -> True    the same sequence
ERROR is BRIGHT_RED_BOLD        # -> False   two objects
DEBUG is DIM                    # -> True    an alias — the very same object
```

**Under the hood:**
```python
DEBUG = DIM                                  # an alias
INFO = BRIGHT_BLUE                           # an alias
SUCCESS = BRIGHT_GREEN + BOLD
WARNING = BRIGHT_YELLOW + BOLD
ERROR = BRIGHT_RED + BOLD
CRITICAL = BG_RED + BRIGHT_WHITE + BOLD      # "41", "97", "1"
```

> 💡 `CRITICAL` is the only level that is not equal to any other preset, because it is the only one
> that sets a background.

[▲ Back to top](#-table-of-contents)

---

### Combining presets

Presets are ordinary styles, so `+` joins them — as many as you like, in any order:

```python
RED + UNDERLINE                         # -> StyleDefiner('31', '4')
BG_BLUE + BRIGHT_WHITE                  # -> StyleDefiner('44', '97')
BG_RED + BRIGHT_WHITE + BOLD            # -> the same as CRITICAL
```

Presets and the [color builders](README_STYLE_COLORS.md) mix freely:

```python
color_hex("#ff8800") + UNDERLINE
BG_BLACK + color_256(208)
```

The order of the codes is the order you write them, so two styles that look the same can still be
two different sequences — see [`__eq__`](README_STYLE_CLASS.md#__eq__-and-__hash__).

[▲ Back to top](#-table-of-contents)

---

### Quick reference — all sixty-two

| Group                      | Count | Presets                                                                          |
|----------------------------|-------|----------------------------------------------------------------------------------|
| Attributes                 | 8     | `BOLD` `DIM` `ITALIC` `UNDERLINE` `BLINK` `REVERSE` `HIDDEN` `STRIKETHROUGH`    |
| Standard colors            | 16    | `BLACK` `RED` `GREEN` `YELLOW` `BLUE` `MAGENTA` `CYAN` `WHITE` and `…_BOLD` of each |
| Bright colors              | 16    | `BRIGHT_BLACK` … `BRIGHT_WHITE` and `BRIGHT_…_BOLD` of each                      |
| Background colors          | 8     | `BG_BLACK` … `BG_WHITE`                                                          |
| Bright background colors   | 8     | `BG_BRIGHT_BLACK` … `BG_BRIGHT_WHITE`                                            |
| Log levels                 | 6     | `DEBUG` `INFO` `SUCCESS` `WARNING` `ERROR` `CRITICAL`                            |

All of them are imported straight from the package:

```python
from simplibs.style import RED, BOLD, BG_BLUE, ERROR
```

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-presets--ready-made-styles)
