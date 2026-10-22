import pkgutil
import sys

import pytest
# Outers
import simplibs.style as style_root
import simplibs.style.presets as presets_package
import simplibs.style.presets.standard_colors as folder
from simplibs.style.base_class import StyleDefiner
from simplibs.style.presets.attributes import BOLD


RESET = "\033[0m"

COLORS = ("BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE")

# Written out by hand from the ANSI standard
EXPECTED: dict[str, tuple[str, ...]] = {
    "BLACK": ("30",),
    "RED": ("31",),
    "GREEN": ("32",),
    "YELLOW": ("33",),
    "BLUE": ("34",),
    "MAGENTA": ("35",),
    "CYAN": ("36",),
    "WHITE": ("37",),
    "BLACK_BOLD": ("30", "1"),
    "RED_BOLD": ("31", "1"),
    "GREEN_BOLD": ("32", "1"),
    "YELLOW_BOLD": ("33", "1"),
    "BLUE_BOLD": ("34", "1"),
    "MAGENTA_BOLD": ("35", "1"),
    "CYAN_BOLD": ("36", "1"),
    "WHITE_BOLD": ("37", "1"),
}


def exported_styles() -> dict[str, StyleDefiner]:
    """Every style the folder exports, by name."""
    return {name: value for name, value in vars(folder).items() if isinstance(value, StyleDefiner)}


def module_names() -> set[str]:
    """The name of every file in the folder (without `__init__`)."""
    return {module.name for module in pkgutil.iter_modules(folder.__path__)}


# ----------------------------------------------------------------------
# The folder as a whole
# ----------------------------------------------------------------------
def test_the_folder_holds_exactly_the_expected_files() -> None:
    assert module_names() == set(EXPECTED)


def test_the_folder_exports_exactly_the_expected_styles() -> None:
    assert set(exported_styles()) == set(EXPECTED)


@pytest.mark.parametrize("name", list(EXPECTED))
def test_every_file_defines_the_style_the_folder_exports(name: str) -> None:
    module = sys.modules[f"{folder.__name__}.{name}"]

    assert getattr(module, name) is exported_styles()[name]


@pytest.mark.parametrize("name", list(EXPECTED))
def test_every_style_is_also_available_from_the_package_and_the_root(name: str) -> None:
    preset = exported_styles()[name]

    assert getattr(presets_package, name) is preset
    assert getattr(style_root, name) is preset


def test_no_two_styles_write_the_same_sequence() -> None:
    sequences = [style.sequence for style in exported_styles().values()]

    assert len(set(sequences)) == len(EXPECTED)


# ----------------------------------------------------------------------
# Each style
# ----------------------------------------------------------------------
@pytest.mark.parametrize("name, codes", list(EXPECTED.items()))
def test_the_style_has_its_codes(name: str, codes: tuple[str, ...]) -> None:
    style = exported_styles()[name]

    assert isinstance(style, StyleDefiner)
    assert style.codes == codes
    assert style.sequence == "\033[" + ";".join(codes) + "m"


@pytest.mark.parametrize("name, codes", list(EXPECTED.items()))
def test_the_style_styles_a_text(name: str, codes: tuple[str, ...]) -> None:
    style = exported_styles()[name]

    assert style("x", use_style=True) == "\033[" + ";".join(codes) + "mx" + RESET
    assert style("x", use_style=False) == "x"


# ----------------------------------------------------------------------
# The relations inside the folder
# ----------------------------------------------------------------------
@pytest.mark.parametrize("color", COLORS)
def test_a_bold_color_is_the_color_plus_bold(color: str) -> None:
    styles = exported_styles()

    assert styles[f"{color}_BOLD"] == styles[color] + BOLD


@pytest.mark.parametrize("color", COLORS)
def test_a_plain_color_is_a_single_code(color: str) -> None:
    assert len(exported_styles()[color].codes) == 1
