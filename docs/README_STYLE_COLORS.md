# 🎨 `style/colors` — Any Color Beyond the Presets

The [presets](README_STYLE_PRESETS.md) cover the sixteen basic colors. Everything else — the
orange of a brand, a color copied from a stylesheet, a gray from a smooth ramp — is built by one
of three functions in this package. Each takes a color in the form you already have it and
returns a ready-to-use [`StyleDefiner`](README_STYLE_CLASS.md).

```python
from simplibs.style import color_256, color_rgb, color_hex

ORANGE = color_hex("#ff8800")

print(ORANGE("Orange text"))
print(color_256(208, background=True)("Orange background"))
print(color_rgb(255, 136, 0)("The same orange, from three numbers"))
```

## A note on the three builders

They differ only in **how you write the color**, never in what you get back:

| Builder        | You write                  | Colors               | Support                                  |
|----------------|----------------------------|----------------------|------------------------------------------|
| `color_256`    | one number `0`–`255`       | 256 (a fixed palette)| Every terminal with more than 16 colors. |
| `color_rgb`    | three numbers `0`–`255`    | 16.7 million         | Terminals with *true color* (most current ones). |
| `color_hex`    | a text such as `"#ff8800"` | 16.7 million         | The same as `color_rgb` — it is `color_rgb`. |

What comes back is an ordinary style, so everything from
[`StyleDefiner`](README_STYLE_CLASS.md) applies: call it, add it to another style, use it as a
dictionary key.

```python
ORANGE_BOLD = color_hex("#ff8800") + BOLD
ORANGE_BOLD("Warning")
```

## A note on terminals

A terminal without true-color support usually shows the **nearest color it has**, or none at all.
The library cannot know what the terminal can do, so it does not
guess: `color_rgb` always writes the true-color sequence. If your output must work everywhere,
choose `color_256` or a [preset](README_STYLE_PRESETS.md).

---

## 🧭 Table of Contents

* [`color_256`](#color_256)
* [`color_rgb`](#color_rgb)
* [`color_hex`](#color_hex)
* [Text or background — the `background` flag](#text-or-background--the-background-flag)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-colors--any-color-beyond-the-presets)

---

### `color_256`

A style for one entry of the 256-color palette. The middle step between the sixteen presets and
full RGB: a single number is easy to write down and to share.

**Parameters:**
* `n` (*int*): The palette index, `0`–`255`.
* `background` (*bool*, keyword-only, default `False`): `True` colors the **background** instead of
  the text.

**Returns:**
* `StyleDefiner`: With the code `38;5;N` (text) or `48;5;N` (background).

**Raises:**
* `ParamError` (`STYLE_COLOR_NOT_INT`): `n` is not an integer (`"208"`, `208.0`, `True`).
* `ParamError` (`STYLE_COLOR_OUT_OF_RANGE`): `n` is outside `0`–`255`.
* `ParamError` (`STYLE_COLOR_BACKGROUND_NOT_BOOL`): `background` is not a `bool`.

**Example usage:**
```python
ORANGE = color_256(208)
ORANGE.sequence                       # -> '\x1b[38;5;208m'
ORANGE("Orange text")

color_256(208, background=True).sequence    # -> '\x1b[48;5;208m'

color_256(256)                        # -> raises: out of range
color_256("208")                      # -> raises: a number, not text
color_256(True)                       # -> raises: a bool is not a number here
```

**What the numbers mean:**

| Index       | What it is                          | Note                                              |
|-------------|-------------------------------------|---------------------------------------------------|
| `0` – `7`   | the standard colors                 | The same as the dark presets (`BLACK` … `WHITE`). |
| `8` – `15`  | the bright colors                   | The same as the `BRIGHT_…` presets.               |
| `16` – `231`| a 6 × 6 × 6 color cube              | Index = `16 + 36·r + 6·g + b`, each of r, g, b is `0`–`5`. |
| `232` – `255`| a gray ramp of 24 shades           | From almost black to almost white.                |

**Under the hood:**
```python
def color_256(n, *, background=False):
    require_color_value(n, "n")                     # an int from 0 to 255, or raises
    introducer = choose_color_introducer(background)  # "38" for text, "48" for background

    return StyleDefiner(f"{introducer};{ANSI.EXTENDED_256};{n}")
```

> 💡 The first sixteen entries are the **terminal's own colors**, so their look depends on the
> user's color scheme. Entries `16`–`255` are fixed, which is why they are the safer choice when a
> color has to look the same everywhere.

[▲ Back to top](#-table-of-contents)

---

### `color_rgb`

A style for any true-color (24-bit) value, written as three channels.

**Parameters:**
* `r` (*int*): Red, `0`–`255`.
* `g` (*int*): Green, `0`–`255`.
* `b` (*int*): Blue, `0`–`255`.
* `background` (*bool*, keyword-only, default `False`): `True` colors the background.

**Returns:**
* `StyleDefiner`: With the code `38;2;R;G;B` (text) or `48;2;R;G;B` (background).

**Raises:**
* `ParamError` (`STYLE_COLOR_NOT_INT`): a channel is not an integer.
* `ParamError` (`STYLE_COLOR_OUT_OF_RANGE`): a channel is outside `0`–`255`.
* `ParamError` (`STYLE_COLOR_BACKGROUND_NOT_BOOL`): `background` is not a `bool`.

**Example usage:**
```python
ORANGE = color_rgb(255, 136, 0)
ORANGE.sequence                           # -> '\x1b[38;2;255;136;0m'
ORANGE("Orange text")

color_rgb(255, 136, 0, background=True).codes     # -> ('48;2;255;136;0',)

color_rgb(255, 136, 300)                  # -> raises: 'b' is out of range
color_rgb(255, "1", 0)                    # -> raises: 'g' is not a number
```

**The failing channel is named.** Each channel is checked on its own, so the error card says
which of `r`, `g` or `b` is wrong and shows its value — not "one of three is wrong".

**Under the hood:**
```python
def color_rgb(r, g, b, *, background=False):
    for value, label in ((r, "r"), (g, "g"), (b, "b")):
        require_color_value(value, label)

    introducer = choose_color_introducer(background)
    return StyleDefiner(f"{introducer};{ANSI.EXTENDED_RGB};{r};{g};{b}")
```

**Under the hood** *(`require_color_value` — one check behind every number)*:
```python
def require_color_value(value, label):
    # True and False are ints in Python, but not colors
    if not isinstance(value, int) or isinstance(value, bool):
        raise_color_not_int_error(label, value)

    if not 0 <= value <= 255:
        raise_color_out_of_range_error(label, value)
```

The type is checked **before** the range: comparing a string with a number would raise a bare
`TypeError` from deep inside Python, while this way the card says what was expected. A `bool` is
refused because `True` would pass the range check and be written into the sequence as the text
`True`.

[▲ Back to top](#-table-of-contents)

---

### `color_hex`

A style for a true color written as a hex string — the form colors arrive in from a design tool, a
stylesheet or a color picker.

**Parameters:**
* `value` (*str*): Six hex digits (`"ff8800"`) or three (`"f80"`, each digit doubled), with or
  without a leading `#`.
* `background` (*bool*, keyword-only, default `False`): `True` colors the background.

**Returns:**
* `StyleDefiner`: Equal to `color_rgb(r, g, b)` of the same color.

**Raises:**
* `ParamError` (`STYLE_COLOR_HEX_INVALID`): `value` is not a hex color string — a `ValueError` for
  a wrong text, a `TypeError` for a value that is not text at all.
* `ParamError` (`STYLE_COLOR_BACKGROUND_NOT_BOOL`): `background` is not a `bool`.

**Accepted forms:**

| You write    | Means                | Note                                    |
|--------------|----------------------|-----------------------------------------|
| `"#ff8800"`  | `255, 136, 0`        | The full form, as copied from a design. |
| `"ff8800"`   | `255, 136, 0`        | Without the `#`.                        |
| `"#f80"`     | `255, 136, 0`        | The short form: every digit is doubled. |
| `"#F80"`     | `255, 136, 0`        | Upper or lower case, both work.         |

**Example usage:**
```python
ORANGE = color_hex("#ff8800")
ORANGE.sequence                       # -> '\x1b[38;2;255;136;0m'

color_hex("f80") == color_rgb(255, 136, 0)      # -> True
color_hex("#ff8800", background=True).sequence  # -> '\x1b[48;2;255;136;0m'

color_hex("orange")                   # -> raises: names are not accepted
color_hex("0xff8800")                 # -> raises: no `0x` prefix
color_hex("#ff8800ff")                # -> raises: a terminal has no transparency
color_hex("#ff880")                   # -> raises: five digits
color_hex(" ff8800")                  # -> raises: no whitespace
color_hex("ff8800\n")                 # -> raises: a newline from a file read is not part of the color
color_hex(0xff8800)                   # -> raises: a number is not a hex text
```

**Strict on purpose.** Every extra spelling is one more way for a typo to be accepted silently,
so the builder takes nothing but the plain forms above. In particular the trailing newline is
refused: a color read line by line from a file should be `.strip()`-ed by the code that reads it.

**It is `color_rgb` in a different spelling.** `color_hex` only parses; the sequence is built by
`color_rgb`, so the two cannot drift apart.

**Under the hood:**
```python
def color_hex(value, *, background=False):
    channels = parse_hex_color(value)            # (r, g, b) or None — never raises
    if channels is None:
        raise_color_hex_invalid_error(value)

    return color_rgb(*channels, background=background)
```

**Under the hood** *(`parse_hex_color` — the one place that knows what a hex color is)*:
```python
HEX_COLOR_PATTERN = re.compile(r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})")

def parse_hex_color(value):
    if not isinstance(value, str):
        return None

    match = HEX_COLOR_PATTERN.fullmatch(value)    # fullmatch: nothing may surround the color
    if match is None:
        return None

    digits = match.group(1)
    if len(digits) == 3:                           # "f80" means "ff8800"
        digits = "".join(digit * 2 for digit in digits)

    return int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)
```

> 💡 The pattern is checked **before** `int(..., 16)` is called. `int("1_0", 16)`, `int(" ff", 16)`
> and `int("+ff", 16)` all succeed, so converting the whole string directly would accept spellings
> that are not colors. The digits are written out as `[0-9a-fA-F]` for the same reason: only ASCII
> hex digits match.

[▲ Back to top](#-table-of-contents)

---

### Text or background — the `background` flag

All three builders take the same keyword-only flag, and it decides one number in the code: `38`
introduces a **text** color, `48` a **background** color. The rest of the sequence is identical.

```python
color_rgb(255, 136, 0).codes                      # -> ('38;2;255;136;0',)
color_rgb(255, 136, 0, background=True).codes     # -> ('48;2;255;136;0',)
```

The flag must be a real `bool`. `background="no"` is a non-empty string, which is truthy, and would
paint the background — the opposite of what was meant, noticed only on the screen. It is refused
the same way `use_style` is in [`StyleDefiner`](README_STYLE_CLASS.md#__call__).

**Under the hood:**
```python
def choose_color_introducer(background):
    if not isinstance(background, bool):
        raise_color_background_not_bool_error(background)

    return ANSI.BG_EXTENDED if background else ANSI.FG_EXTENDED     # "48" or "38"
```

A text color and a background color are two styles that combine with `+`:

```python
BADGE = color_hex("#ffffff") + color_hex("#cc0000", background=True) + BOLD
BADGE(" FAILED ")
```

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

Every error is a structured [`ParamError`](https://pypi.org/project/simplibs-exception/) card; the
name starts with `STYLE_`.

| Error name                        | Wraps                    | Raised by                              | When                                              |
|-----------------------------------|--------------------------|----------------------------------------|---------------------------------------------------|
| `STYLE_COLOR_NOT_INT`             | `TypeError`              | `color_256`, `color_rgb`               | A value is not an integer (`"208"`, `208.0`, `True`). |
| `STYLE_COLOR_OUT_OF_RANGE`        | `ValueError`             | `color_256`, `color_rgb`               | An integer outside `0`–`255`.                     |
| `STYLE_COLOR_HEX_INVALID`         | `ValueError` / `TypeError` | `color_hex`                          | Not a hex color: wrong text (`ValueError`), not text (`TypeError`). |
| `STYLE_COLOR_BACKGROUND_NOT_BOOL` | `TypeError`              | `color_256`, `color_rgb`, `color_hex`  | `background` is not a `bool`.                     |

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-colors--any-color-beyond-the-presets)