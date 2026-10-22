# 🚦 `style/settings` — Whether Styles Are Applied

Every call of a style asks one question: *should I really write the escape codes, or hand the
text back plain?* The `settings` package answers it. Text sent into a file, a pipe or a test
should carry no `\033[91m`; text sent to a real terminal should. This package makes that decision
for you — and lets you overrule it, for the whole program or for one block.

```python
from simplibs.style import RED, set_styles_enabled, styles_disabled

print(RED("Styled when the output is a terminal, plain otherwise"))

set_styles_enabled(False)              # the whole program: no styles at all

with styles_disabled():                # only this block: plain text, always
    report = RED("goes into a file")
```

## A note on the layers

Two mechanisms work together, and a third one sits above them:

| Layer                 | Scope                                  | Moved by                                          |
|-----------------------|----------------------------------------|---------------------------------------------------|
| `use_style=` argument | **one call** of a style                | `RED("x", use_style=False)`                       |
| scoped override       | one `with` block, **per thread/task**  | `styles_disabled()` / `styles_enabled()`          |
| process-wide switch   | the **whole program**, every thread    | `set_styles_enabled()` / `reset_styles_enabled()` |

The more specific layer always wins: `use_style=` beats an override, an override beats the
process-wide switch, and the switch starts from what the environment says (see
[The starting position](#the-starting-position)).

```python
set_styles_enabled(False)              # the switch says: plain

with styles_enabled():                 # the override says: styled
    RED("a")                           # -> styled
    RED("b", use_style=False)          # -> plain      the argument beats the override
```

## A note on why there are two kinds of "off"

A new thread starts with an **empty context**, so a setting kept in a context variable and made in
the main thread would silently not reach it. That is why the process-wide switch lives in one
shared holder (every thread sees the same position), and only the temporary `with` overrides are
per thread or async task. Two tasks can therefore print in different modes at the same moment, and
`set_styles_enabled(False)` in `main()` still holds for the worker threads you start later.

---

## 🧭 Table of Contents

* [The starting position](#the-starting-position)
* [`get_styles_enabled`](#get_styles_enabled)
* [`set_styles_enabled`](#set_styles_enabled)
* [`reset_styles_enabled`](#reset_styles_enabled)
* [`styles_disabled`](#styles_disabled)
* [`styles_enabled`](#styles_enabled)
* [The `with` manager — decorator, nesting, threads](#the-with-manager--decorator-nesting-threads)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-settings--whether-styles-are-applied)

---

### The starting position

When the library is imported, the process-wide switch is set from the **environment**. The same
decision is made again by [`reset_styles_enabled`](#reset_styles_enabled). The checks run in this
order, and the first one that applies decides:

| # | Check                                         | Result  | Why                                                           |
|---|-----------------------------------------------|---------|---------------------------------------------------------------|
| 1 | `NO_COLOR` is set and not empty               | **off** | The user's explicit refusal — it beats everything.            |
| 2 | `FORCE_COLOR` is set and not empty            | **on**  | The explicit request, e.g. for CI logs that render colors.    |
| 3 | `TERM` is `dumb`                              | **off** | A terminal that would print the escape codes as visible text. |
| 4 | standard output is an interactive terminal    | **on**  | A real terminal gets styles; a pipe, a file or a test does not. |
| — | none of the above                             | **off** |                                                               |

**Example usage:**
```python
# in a terminal                           -> styles on
# python script.py > out.txt              -> styles off   (output is a file)
# NO_COLOR=1 python script.py             -> styles off   (even in a terminal)
# FORCE_COLOR=1 python script.py > out.txt -> styles on   (even into a file)
```

**What "set" means.** A variable counts when it exists and holds more than whitespace. Its value is
**not interpreted**: `NO_COLOR=0` still means "no color" — the convention looks at presence, not at
what follows the `=`. (See [no-color.org](https://no-color.org) and
[force-color.org](https://force-color.org).)

**Standard output only.** The default follows `stdout`. A program that styles only its error
stream can call `set_styles_enabled(True)` or use `styles_enabled()`.

**It never raises.** A captured stream (as in `pytest`), a closed stream or a missing `sys.stdout`
(a windowed application) simply answer "not a terminal", so importing the library never fails
because of where its output goes.

**Under the hood** *(`should_enable_styles_by_default`)*:
```python
def should_enable_styles_by_default() -> bool:
    if _is_env_flag_set("NO_COLOR"):
        return False
    if _is_env_flag_set("FORCE_COLOR"):
        return True
    if _is_dumb_terminal():
        return False
    return _is_stdout_terminal()
```

> 💡 Nothing is cached here. The switch calls this function once at import, and
> `reset_styles_enabled` calls it again on demand.

[▲ Back to top](#-table-of-contents)

---

### `get_styles_enabled`

The one question every style asks: *are styles on right now?* Use it when your own code needs to
know — for example to decide whether to draw a progress bar with colors or without.

**Parameters:**
* *(none)*

**Returns:**
* `bool`: The scoped override when one is active, otherwise the process-wide switch.

**Example usage:**
```python
get_styles_enabled()                   # -> True in a terminal, False in a pipe

with styles_disabled():
    get_styles_enabled()               # -> False
```

**Under the hood:**
```python
def get_styles_enabled() -> bool:
    override = STYLES_OVERRIDE.get()
    if override is not None:
        return override

    return GLOBAL_STYLES_SWITCH.enabled
```

The override is read **first**: the block of `with styles_disabled():` must stay plain even when
the switch says otherwise. It is two lookups and a comparison because every styled text asks.

> 💡 The argument `use_style=` of a style is **not** part of this function. A style resolves
> `use_style` itself and calls `get_styles_enabled()` only when `use_style` is `None`.

[▲ Back to top](#-table-of-contents)

---

### `set_styles_enabled`

Moves the process-wide switch. One call at the start of a program — for example from a
`--no-color` option — and it holds for every thread and every part of the program.

**Parameters:**
* `value` (*bool*): `True` to style text, `False` to pass it through unchanged.

**Returns:**
* `None`

**Raises:**
* `ParamError` (`STYLE_STYLES_ENABLED_NOT_BOOL`): `value` is not a `bool`.

**Example usage:**
```python
set_styles_enabled(False)              # a --no-color option
RED("x")                               # -> 'x'

set_styles_enabled(True)               # force styles on, even into a file
RED("x")                               # -> '\x1b[31mx\x1b[0m'

set_styles_enabled(1)                  # -> raises: only True or False
set_styles_enabled("no")               # -> raises: "no" would be read as true
```

**A scoped override still wins.** Called inside `with styles_disabled():`, the call moves the
switch, but the block stays plain until it ends. That is the point of an override.

```python
with styles_disabled():
    set_styles_enabled(True)
    get_styles_enabled()               # -> False    the block still decides
get_styles_enabled()                   # -> True     the switch was moved
```

**Why only a real `bool`.** `set_styles_enabled("no")` would store a non-empty string and be
read as truthy — the mistake would show up as colors where there should be none, far from the call
that caused it.

**Under the hood:**
```python
def set_styles_enabled(value: bool) -> None:
    if not isinstance(value, bool):
        raise_styles_enabled_not_bool_error(value)

    GLOBAL_STYLES_SWITCH.enabled = value
```

`GLOBAL_STYLES_SWITCH` is a small holder object (`StylesSwitch`) with one attribute, not a plain
module-level `bool`: after `from x import SWITCH` every importer would hold **its own copy** of a
`bool`, while a holder is shared by identity, so what this function writes is what
`get_styles_enabled` reads in every module and thread. It needs no lock — assigning one attribute
is a single step in Python and the switch holds one independent value.

[▲ Back to top](#-table-of-contents)

---

### `reset_styles_enabled`

Puts the process-wide switch back to what the **environment** says. It undoes every
`set_styles_enabled`.

**Parameters:**
* *(none)*

**Returns:**
* `None`

**Example usage:**
```python
set_styles_enabled(True)
reset_styles_enabled()                 # back to: terminal -> on, pipe -> off
```

Used mostly in tests, which must not leak a setting into the next test:

```python
@pytest.fixture(autouse=True)
def _clean_styles():
    yield
    reset_styles_enabled()
```

**The environment is read again.** The starting position is computed once at import; a reset
computes it anew, so a changed `NO_COLOR` or a redirected output is noticed.

```python
os.environ["NO_COLOR"] = "1"
reset_styles_enabled()
get_styles_enabled()                   # -> False
```

**Under the hood:**
```python
def reset_styles_enabled() -> None:
    GLOBAL_STYLES_SWITCH.enabled = should_enable_styles_by_default()
```

[▲ Back to top](#-table-of-contents)

---

### `styles_disabled`

Plain text for one block, one decorated function — no escape codes, whatever the switch and the
environment say.

**Parameters:**
* *(none)*

**Returns:**
* `StylesOverride`: A manager for a `with` statement (or a decorator). It is **not** a yes/no value
  — see [the `with` manager](#the-with-manager--decorator-nesting-threads).

**Example usage:**
```python
with styles_disabled():
    print(RED("this prints as plain text"))

@styles_disabled()
def render_report() -> str:
    return RED("title") + "\n" + GREEN("body")      # no escape codes in the result
```

Typical uses: text written to a file, copied into a message, or compared in a test.

The change holds for the **current thread or async task** only, and the previous state is
restored when the block ends — **even after an exception**.

**Under the hood:**
```python
def styles_disabled() -> StylesOverride:
    return StylesOverride(False)
```

[▲ Back to top](#-table-of-contents)

---

### `styles_enabled`

The counterpart: styled text for one block, even when the output is not a terminal.

**Parameters:**
* *(none)*

**Returns:**
* `StylesOverride`: A manager for a `with` statement (or a decorator).

**Example usage:**
```python
with styles_enabled():
    text = RED("always carries the escape codes")

text                                   # -> '\x1b[31malways carries the escape codes\x1b[0m'
```

The natural place for it is a **test of styled output**. Tests run with captured, non-terminal
output, where styling is off by default; wrapping the test in this block makes the expected
escape codes appear without touching the process-wide switch.

```python
def test_error_is_red():
    with styles_enabled():
        assert RED("x") == "\033[31mx\033[0m"
```

**Stronger than the environment.** It overrides `NO_COLOR` as well. A block that asks for styling
explicitly means it — the person who wrote the block is the one who decides.

**Under the hood:**
```python
def styles_enabled() -> StylesOverride:
    return StylesOverride(True)
```

> 💡 Despite its name it is **not** a getter. `get_styles_enabled()` answers the question; this one
> opens a block.

[▲ Back to top](#-table-of-contents)

---

### The `with` manager — decorator, nesting, threads

`styles_disabled()` and `styles_enabled()` both return a `StylesOverride`. It is a small class, but
its behavior is worth knowing.

**Scope: the current thread or async task.** The override is stored in a `ContextVar`, so it holds
for the code that runs inside the block — and **not** for another thread started from it:

```python
with styles_disabled():
    threading.Thread(target=worker).start()    # the worker follows the process-wide switch
```

Two async tasks can sit in opposite modes at the same moment without disturbing each other:

```python
async def plain():
    with styles_disabled():
        await asyncio.sleep(0.1)
        return get_styles_enabled()            # -> False

async def styled():
    with styles_enabled():
        await asyncio.sleep(0.1)
        return get_styles_enabled()            # -> True

await asyncio.gather(plain(), styled())        # -> [False, True]
```

**Nesting.** The inner block wins, and the outer one is restored when it ends:

```python
with styles_disabled():
    with styles_enabled():
        get_styles_enabled()                   # -> True
    get_styles_enabled()                       # -> False
```

Entering the **same** manager twice (`with m: with m:`) is safe too — each entry keeps its own
undo token and each exit undoes the latest one.

**As a decorator.** `@styles_disabled()` wraps a plain function; every call of it gets a **fresh**
manager, so threads and recursion never share one stack of tokens.

```python
@styles_disabled()
def render_report() -> str: ...
```

Only plain functions are wrapped. An `async def` needs a `with` block **inside** it.

**It refuses to be a question.** Any object is truthy by default, so
`if styles_enabled():` would always pass and quietly do the wrong thing. The manager raises instead:

```python
if styles_enabled():                   # -> raises STYLE_OVERRIDE_USED_AS_BOOL
    ...

if get_styles_enabled():               # the way to ask
    ...
```

**Under the hood:**
```python
class StylesOverride(ContextDecorator):
    def __init__(self, value: bool) -> None:
        self._value = value
        self._tokens: list[Token] = []

    def _recreate_cm(self) -> "StylesOverride":      # a fresh manager for every decorated call
        return StylesOverride(self._value)

    def __enter__(self) -> None:
        self._tokens.append(STYLES_OVERRIDE.set(self._value))

    def __exit__(self, *exc_info) -> None:
        STYLES_OVERRIDE.reset(self._tokens.pop())    # however the block ended

    def __bool__(self) -> bool:
        raise_styles_override_used_as_bool_error()
```

`STYLES_OVERRIDE` is `ContextVar("STYLES_OVERRIDE", default=None)` — `None` means *no override,
ask the switch*. A third state is needed because `False` is a real answer, not an absence.

**Why a class and not `@contextmanager`.** With a generator-based manager there is no place for
`__bool__`, and the name that reads like a question would silently be an answer to none.

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

Every error is a structured [`ParamError`](https://pypi.org/project/simplibs-exception/) card; the
name starts with `STYLE_`.

| Error name                      | Wraps       | Raised by                                | When                                                   |
|---------------------------------|-------------|------------------------------------------|--------------------------------------------------------|
| `STYLE_STYLES_ENABLED_NOT_BOOL` | `TypeError` | `set_styles_enabled`                     | `value` is not a `bool` (`1`, `"no"`, `None`).         |
| `STYLE_OVERRIDE_USED_AS_BOOL`   | `TypeError` | `styles_disabled()`, `styles_enabled()`  | The manager is used as a yes/no value (`if ...:`).     |

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-settings--whether-styles-are-applied)
