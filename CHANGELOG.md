# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-10-20

### ✨ Added

#### Base Class

* `StyleDefiner(*codes)` — immutable terminal text style built from one or more ANSI codes, called like a function (`RED("text")`) and combined with `+` (`RED + BOLD`)
* Accepts a code as `"91"`, `"91m"` or the full `"\033[91m"`, multi-part codes such as `"38;5;208"`, and other `StyleDefiner` instances
* Read-only `codes` (bare codes) and `sequence` (ready escape sequence); equality and hash follow the sequence; `repr` can be pasted back as code
* `sum([...])` support for combining a list of styles
* Per-call override `use_style=True | False` to force or skip styling for a single call
* Nested styles keep the outer style after an inner one ends: `RED("a " + BOLD("b") + " c")` stays red after `b`
* The result is always a `str`; non-string input is converted with `str()`, and an empty text stays empty

#### Color Builders

* `color_256(n, *, background=False)` — color from the 256-color palette
* `color_rgb(r, g, b, *, background=False)` — true-color (24-bit) RGB color
* `color_hex(value, *, background=False)` — true color from `"#rrggbb"`, `"rrggbb"`, `"#rgb"` or `"rgb"`

#### Settings

* `get_styles_enabled()` — the current answer to "are styles applied?"
* `set_styles_enabled(value)` — switches styling on or off for the whole process, every thread included
* `reset_styles_enabled()` — returns the process-wide switch to what the environment says
* `styles_disabled()` and `styles_enabled()` — context managers (also usable as decorators) that disable or force styling for one block, scoped to the current thread or async task (`ContextVar`-backed) and restored even after an exception
* Using one of these managers as a yes/no value (`if styles_enabled():`) is refused with an error instead of silently always passing — the question is asked with `get_styles_enabled()`
* Environment-aware default: `NO_COLOR` disables styles, `FORCE_COLOR` enables them, `TERM=dumb` disables them, and otherwise styles are applied only when standard output is an interactive terminal (pipes, files and captured output stay plain)

#### Presets

* Sixty-two ready-made `StyleDefiner` instances, one per file, each with a full docstring for editor hover help
* Attributes: `BOLD`, `DIM`, `ITALIC`, `UNDERLINE`, `BLINK`, `REVERSE`, `HIDDEN`, `STRIKETHROUGH`
* Standard colors: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE` and their bold variants (`RED_BOLD`...)
* Bright colors: `BRIGHT_BLACK` ... `BRIGHT_WHITE` and their bold variants (`BRIGHT_RED_BOLD`...)
* Backgrounds: `BG_BLACK` ... `BG_WHITE` and `BG_BRIGHT_BLACK` ... `BG_BRIGHT_WHITE`
* Log levels: `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`
* All presets are exported from the package root and from `simplibs.style.presets`

#### Constants

* `ANSI` — table of all 56 standard SGR codes (attributes, `*_OFF` codes, standard and bright foreground and background colors, extended color introducers)
* `ESCAPE_PREFIX`, `ESCAPE_SUFFIX`, `RESET_SEQUENCE` — the parts of a style sequence, available from `simplibs.style.constants`

#### Exceptions

* The library defines no exceptions of its own; every invalid argument raises `ParamError` from `simplibs-exception`, which is also catchable as the native `TypeError` or `ValueError` it wraps
* Error names: `STYLE_NO_CODES`, `STYLE_CODE_NOT_TEXT`, `STYLE_EMPTY_CODE`, `STYLE_INVALID_ANSI_FORMAT`, `STYLE_INVALID_CODE`, `STYLE_USE_STYLE_NOT_BOOL`, `STYLE_COLOR_NOT_INT`, `STYLE_COLOR_OUT_OF_RANGE`, `STYLE_COLOR_HEX_INVALID`, `STYLE_COLOR_BACKGROUND_NOT_BOOL`, `STYLE_STYLES_ENABLED_NOT_BOOL`, `STYLE_OVERRIDE_USED_AS_BOOL`

#### Typing

* `py.typed` marker — the package ships its type information (declared in `package-data`, so it is part of the built wheel)

#### Documentation

* Main `README.md` with a quick start in four levels, the package structure, a quick reference and the table of all error names
* Detailed references in `docs/`: `README_STYLE_CLASS`, `README_STYLE_SETTINGS`, `README_STYLE_COLORS`, `README_STYLE_PRESETS` and `README_STYLE_CONSTANTS` — one card per function or method, with a view under the hood

#### Tests & CI

* GitHub Actions workflow (`.github/workflows/tests.yml`) running the test suite with coverage on Linux, Windows and macOS with Python 3.11, 3.12 and 3.13, and a `tests` badge in the README
* `dev` extra: `pytest>=9.0` (the `subtests` fixture is built in since pytest 9.0) and `pytest-cov>=5.0`

#### Dependencies

* `simplibs-exception` — structured diagnostic output behind every raised `ParamError`

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)