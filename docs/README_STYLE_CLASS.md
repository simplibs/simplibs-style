# 🧱 `style/base_class` — `StyleDefiner`, the One Class of the Library

`StyleDefiner` is the single class everything in `simplibs-style` is built on. A preset
(`RED`, `BOLD`, `ERROR`), a color from a builder (`color_hex("#ff8800")`) and a style you
define yourself are all the same thing: an immutable object that holds one or more ANSI codes
and is **called like a function** to style a text.

It does three jobs and nothing else:

1. **Holds the codes** of a style and the escape sequence built from them (`codes`, `sequence`).
2. **Applies the style** to a text when called — or hands the text back unchanged when styling
   is switched off (`__call__`).
3. **Combines** with other styles through the plain `+` operator (`__add__`, `__radd__`).

```python
from simplibs.style import StyleDefiner

RED = StyleDefiner("91")
BOLD = StyleDefiner("1")
ERROR = RED + BOLD

print(ERROR("Something went wrong"))
```

## A note on immutability

A style is **read-only** after it is created: `codes` and `sequence` are properties without a
setter, and combining two styles builds a **new** object instead of changing one of them. This is
deliberate — a preset such as `RED` is imported by every module that uses it, so a style that
could be changed in one place would change in all of them. The same fact is what lets a style
be a dictionary key or a set member (see [`__eq__` and `__hash__`](#__eq__-and-__hash__)).

## A note on bare codes

A style stores its **bare codes** (`"91"`, `"1"`), never the finished escape sequence of another
style. That is what makes `RED + BOLD` work: combining joins the bare codes into `\033[91;1m`,
instead of nesting one finished sequence into another. The sequence itself is built once, in the
constructor, from the codes.

---

## 🧭 Table of Contents

* [`StyleDefiner(*codes)`](#styledefinercodes)
* [`codes`](#codes)
* [`sequence`](#sequence)
* [`__call__`](#__call__)
* [`__add__` / `__radd__`](#__add__--__radd__)
* [`__eq__` and `__hash__`](#__eq__-and-__hash__)
* [`__repr__`](#__repr__)
* [Errors of this class](#errors-of-this-class)

[⬅️ Back to main README](../README.md#-the-styledefiner-class)

---

### `StyleDefiner(*codes)`

Builds a style from one or more ANSI codes and/or other styles.

**Parameters:**
* `*codes` (*str | StyleDefiner*): At least one entry. Each entry is either a **code** in one of
  the shapes below, or another `StyleDefiner` whose codes are taken over.

**Accepted shapes of a code:**

| You write          | Stored as    | Note                                                          |
|--------------------|--------------|---------------------------------------------------------------|
| `"91"`             | `"91"`       | The bare code.                                                |
| `"91m"`            | `"91"`       | With the closing `m`.                                         |
| `"\033[91m"`       | `"91"`       | The complete escape sequence, as copied from a manual.        |
| `"38;5;208"`       | `"38;5;208"` | A multi-part code: digits joined by single semicolons.        |
| `RED`              | `"91"` …     | Another style; its already normalized codes are taken over.   |

**Raises:**
* `ParamError` (`STYLE_NO_CODES`): no entry was given.
* `ParamError` (`STYLE_CODE_NOT_TEXT`): an entry is neither a string nor a `StyleDefiner` (`91`).
* `ParamError` (`STYLE_EMPTY_CODE`): an entry has no digits in it (`""`, `"   "`, `"m"`, `"\033[m"`).
* `ParamError` (`STYLE_INVALID_ANSI_FORMAT`): an entry starts like an escape sequence but does not
  end with `m` (`"\033[2J"` clears the screen, it is not a style).
* `ParamError` (`STYLE_INVALID_CODE`): an entry is anything other than digits joined by single
  semicolons (`"9x"`, `";;"`, `"1;"`).

**Example usage:**
```python
StyleDefiner("91")                    # -> StyleDefiner('91')
StyleDefiner("91m").codes             # -> ('91',)
StyleDefiner("\033[91m").codes        # -> ('91',)
StyleDefiner("38;5;208").sequence     # -> '\x1b[38;5;208m'

StyleDefiner(RED, BOLD).codes         # -> ('31', '1')       styles are taken over

StyleDefiner()                        # -> raises: a style needs at least one code
StyleDefiner(91)                      # -> raises: a code is text, '91' not 91
StyleDefiner("m")                     # -> raises: nothing in front of the 'm'
StyleDefiner("\033[2J")               # -> raises: not a style sequence
```

**Why a style without a code is refused.** `StyleDefiner()` would write `\033[m`, which is the
*reset* sequence — a style that silently switches everything off is the opposite of what anyone
means by creating one. For the same reason `"m"` and `"\033[m"` are reported as empty, not as
valid.

**The value of a code is not range-checked.** `StyleDefiner("999")` is accepted: a terminal ignores
a code it does not know, and the list of known codes changes. What the library guards is the
**shape** — digits and semicolons — because a malformed code is not ignored by a terminal; it
shows up as strange characters on the screen, far from the line that caused it.

**Under the hood** *(the constructor)*:
```python
def __init__(self, *codes):
    if not codes:
        raise_no_codes_error()

    parts: list[str] = []
    for entry in codes:
        if isinstance(entry, StyleDefiner):
            parts.extend(entry.codes)               # already normalized
        else:
            parts.append(normalize_code(entry))     # or raises

    self._codes = tuple(parts)
    self._sequence = f"{ESCAPE_PREFIX}{';'.join(parts)}{ESCAPE_SUFFIX}"
```

**Under the hood** *(`normalize_code` — one code, one shape)*:
```python
def normalize_code(code):
    if not isinstance(code, str):
        raise_code_not_text_error(code)

    body = code
    if code.startswith(ESCAPE_PREFIX):                  # "\033[91m"
        if not code.endswith(ESCAPE_SUFFIX):
            raise_invalid_ansi_format_error(code)
        body = code[len(ESCAPE_PREFIX):-len(ESCAPE_SUFFIX)]
    elif code.endswith(ESCAPE_SUFFIX):                  # "91m"
        body = code[:-len(ESCAPE_SUFFIX)]

    if not body.strip():
        raise_empty_code_error(code)
    if CODE_PATTERN.fullmatch(body) is None:            # [0-9]+(?:;[0-9]+)*
        raise_invalid_code_error(code)

    return body
```

> 💡 The pattern uses `[0-9]`, not `\d` or `str.isdigit()`. Those accept digits of other scripts
> and characters like `²`, and a terminal understands none of them.

[▲ Back to top](#-table-of-contents)

---

### `codes`

A **read-only property**: the bare codes of the style, in the order they were given.

**Type:**
* `tuple[str, ...]`: One string per code. Combining styles keeps the pieces apart — see the note
  under `__eq__`.

**Example usage:**
```python
RED.codes                  # -> ('31',)
(RED + BOLD).codes         # -> ('31', '1')
StyleDefiner("31;1").codes # -> ('31;1',)     one code written with a semicolon stays one entry
```

**Under the hood:**
```python
@property
def codes(self) -> tuple[str, ...]:
    return self._codes
```

[▲ Back to top](#-table-of-contents)

---

### `sequence`

A **read-only property**: the escape sequence that switches the style on. It is built **once**,
in the constructor, so reading it costs nothing.

**Type:**
* `str`: `ESC`, `[`, the codes joined by `;`, and `m`.

**Example usage:**
```python
RED.sequence                       # -> '\x1b[31m'
(RED + BOLD).sequence              # -> '\x1b[31;1m'
color_256(208).sequence            # -> '\x1b[38;5;208m'
```

**Under the hood:**
```python
@property
def sequence(self) -> str:
    return self._sequence
```

> 💡 Most code never needs it — calling the style is enough. It is there for the places where you
> assemble the output yourself, and for tests that check what a style writes.

[▲ Back to top](#-table-of-contents)

---

### `__call__`

Applies the style to a text. This is the line that runs every time something is printed, so it
does only what it must.

**Parameters:**
* `text` (*Any*): The text to style. Anything that is not a string is converted with `str()` first.
* `use_style` (*bool | None*, keyword-only, default `None`): Decides for **this one call**
  whether the style is applied.
  * `None` — follow the current setting (`get_styles_enabled()`, see
    [`README_STYLE_SETTINGS`](README_STYLE_SETTINGS.md)).
  * `True` — style the text, whatever the setting says.
  * `False` — return the text plain, whatever the setting says.

**Returns:**
* `str`: The styled text — or the same text, unchanged, when styling is off. **Always a string**,
  so the caller can rely on the type either way.

**Raises:**
* `ParamError` (`STYLE_USE_STYLE_NOT_BOOL`): `use_style` is neither `None` nor a `bool`.

**Example usage:**
```python
RED("Error", use_style=True)       # -> '\x1b[31mError\x1b[0m'
RED("Error", use_style=False)      # -> 'Error'
RED(404, use_style=True)           # -> '\x1b[31m404\x1b[0m'      numbers are converted
RED("", use_style=True)            # -> ''                        nothing to style, nothing written

RED("x", use_style="no")           # -> raises: only True, False or None decide
```

**Styles inside styles.** A text that already contains a styled part keeps the outer style after it:

```python
RED("a " + BOLD("b") + " c", use_style=True)
# -> '\x1b[31ma \x1b[1mb\x1b[0m\x1b[31m c\x1b[0m'
#                         └── the reset of BOLD is followed by red again
```

Without that step the reset that closes `BOLD("b")` would also end the red, and ` c` would come
out plain.

* Every spelling of the **lone** reset is recognized: `\033[0m`, `\033[00m` and `\033[m` — the
  last two come from other tools (`git diff --color`, `ls --color`, shell prompts), so styling
  their output works too.
* A reset combined with other codes (`\033[0;1m`) and a partial reset such as `\033[39m` are
  **left alone**. What the outer style should become after them is a guess, and the library does
  not rewrite sequences it did not write.

**Why `use_style="no"` is refused.** A non-empty string is truthy, so `"no"` would switch styling
**on** — the opposite of what was meant. The mistake is stopped where it is made.

**Under the hood** *(`__call__`)*:
```python
def __call__(self, text, *, use_style=None):
    if use_style is None:
        enabled = get_styles_enabled()
    elif isinstance(use_style, bool):
        enabled = use_style
    else:
        raise_use_style_not_bool_error(use_style)

    text = str(text)
    return apply_style(self._sequence, text) if enabled else text
```

**Under the hood** *(`apply_style`)*:
```python
def apply_style(sequence, text):
    if not text:
        return text                                   # an empty text stays empty

    if ESCAPE_PREFIX in text:                         # only a text with an escape is searched
        text = RESET_PATTERN.sub(
            lambda match: f"{match.group(0)}{sequence}", text
        )                                             # switch this style back on after every reset

    return f"{sequence}{text}{RESET_SEQUENCE}"
```

> 💡 `RESET_PATTERN` is `ESCAPE_PREFIX` + `0*` + `ESCAPE_SUFFIX`, built from the constants, so the
> frame of a sequence still has exactly one definition.

[▲ Back to top](#-table-of-contents)

---

### `__add__` / `__radd__`

Combines two styles with `+`. The result is a **new** style whose codes are the codes of the left
one followed by the codes of the right one.

**Parameters:**
* `other` (*StyleDefiner*): The style to add.

**Returns:**
* `StyleDefiner`: A new style, or `NotImplemented` if `other` is not a style — Python then raises
  its own, familiar `TypeError`.

**Example usage:**
```python
ERROR = RED + BOLD
ERROR.codes                        # -> ('31', '1')
ERROR.sequence                     # -> '\x1b[31;1m'

CRITICAL = BG_RED + BRIGHT_WHITE + BOLD       # any number of styles in a chain

sum([RED, BOLD, UNDERLINE])        # -> StyleDefiner('31', '1', '4')

RED + "text"                       # -> TypeError: unsupported operand type(s) for +
```

**Why `__radd__` exists.** One case only: the built-in `sum()`. It starts its accumulator at the
integer `0`, so `sum([RED, BOLD])` first asks `0 + RED`. `__radd__` accepts exactly that value and
returns the style itself; anything else — `1`, `None`, a `bool` — is refused with `NotImplemented`.

**Order is kept.** `RED + BOLD` writes `\033[31;1m` and `BOLD + RED` writes `\033[1;31m`. They look
the same, but they are different sequences, so they are not equal (see
[`__eq__`](#__eq__-and-__hash__)). When two codes of the *same kind* meet (two colors), the
terminal lets the later one win: `RED + BLUE` is blue.

**Under the hood:**
```python
def __add__(self, other):
    if not isinstance(other, StyleDefiner):
        return NotImplemented
    return StyleDefiner(self, other)          # the constructor joins the bare codes

def __radd__(self, other):
    if type(other) is int and other == 0:     # only the start value of sum(); a bool is not an int here
        return self
    return NotImplemented
```

[▲ Back to top](#-table-of-contents)

---

### `__eq__` and `__hash__`

Two styles are equal when they **write the same escape sequence**. The hash follows the
sequence, so a style can be a dictionary key or a member of a set.

**Returns:**
* `__eq__` → `bool`, or `NotImplemented` when the other side is not a style.
* `__hash__` → `int`: the hash of `sequence`.

**Example usage:**
```python
RED == StyleDefiner("31")                      # -> True
RED + BOLD == StyleDefiner("31;1")             # -> True    same bytes, different split of `codes`
(RED + BOLD).codes == StyleDefiner("31;1").codes   # -> False   ('31', '1') vs ('31;1',)

ERROR == BRIGHT_RED_BOLD                       # -> True    a preset by meaning equals the preset by look
RED + BOLD == BOLD + RED                       # -> False   a different order is a different sequence

levels = {ERROR: "red", INFO: "blue"}          # styles as dictionary keys
```

> 💡 Equality compares the **sequence**, not the `codes`, because the sequence is what the
> terminal receives. `StyleDefiner("31;1")` and `RED + BOLD` differ in how the codes are split and
> still produce the very same output.

**Under the hood:**
```python
def __eq__(self, other):
    if not isinstance(other, StyleDefiner):
        return NotImplemented
    return self._sequence == other._sequence

def __hash__(self):
    return hash(self._sequence)
```

[▲ Back to top](#-table-of-contents)

---

### `__repr__`

A debugging convenience: the style written the way you would create it.

**Returns:**
* `str`: `StyleDefiner('<code>', '<code>', ...)`.

**Example usage:**
```python
repr(RED)                  # -> "StyleDefiner('31')"
repr(RED + BOLD)           # -> "StyleDefiner('31', '1')"
```

**Under the hood:**
```python
def __repr__(self):
    return f"StyleDefiner({', '.join(repr(code) for code in self._codes)})"
```

`repr` shows the **codes**, not the raw escape sequence. In a log or a failed test the sequence
would be printed as an invisible mess (or, worse, would style the line it is printed on), while
the codes read — and can be pasted back — as the code that creates the style.

[▲ Back to top](#-table-of-contents)

---

### Errors of this class

Every error is a structured [`ParamError`](https://pypi.org/project/simplibs-exception/) card; the
name starts with `STYLE_`.

| Error name                  | Wraps        | Raised by                | When                                                     |
|-----------------------------|--------------|--------------------------|----------------------------------------------------------|
| `STYLE_NO_CODES`            | `ValueError` | `StyleDefiner(...)`      | No entry was given.                                      |
| `STYLE_CODE_NOT_TEXT`       | `TypeError`  | `StyleDefiner(...)`      | An entry is not a string or a `StyleDefiner`.            |
| `STYLE_EMPTY_CODE`          | `ValueError` | `StyleDefiner(...)`      | An entry has no digits in it (`""`, `"m"`, `"\033[m"`).  |
| `STYLE_INVALID_ANSI_FORMAT` | `ValueError` | `StyleDefiner(...)`      | An escape sequence that does not end with `m`.           |
| `STYLE_INVALID_CODE`        | `ValueError` | `StyleDefiner(...)`      | Anything but digits joined by single semicolons.         |
| `STYLE_USE_STYLE_NOT_BOOL`  | `TypeError`  | `__call__`               | `use_style` is neither `None` nor a `bool`.              |

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-the-styledefiner-class)
