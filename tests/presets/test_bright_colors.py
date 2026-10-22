import pkgutil
import sys

import pytest
# Outers
import simplibs.style as style_root
import simplibs.style.presets as presets_package
import simplibs.style.presets.bright_colors as folder
from simplibs.style.base_class import StyleDefiner
from simplibs.style.presets.attributes import BOLD


RESET = "\033[0m"

COLORS = ("BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE")

# Written out by hand from the ANSI standard
EXPECTED: dict[str, tuple[str, ...]] = {
    "BRIGHT_BLACK": ("90",),
    "BRIGHT_RED": ("91",),
    "BRIGHT_GREEN": ("92",),
    "BRIGHT_YELLOW": ("93",),
    "BRIGHT_BLUE": ("94",),
    "BRIGHT_MAGENTA": ("95",),
    "BRIGHT_CYAN": ("96",),
    "BRIGHT_WHITE": ("97",),
    "BRIGHT_BLACK_BOLD": ("90", "1"),
    "BRIGHT_RED_BOLD": ("91", "1"),
    "BRIGHT_GREEN_BOLD": ("92", "1"),
    "BRIGHT_YELLOW_BOLD": ("93", "1"),
    "BRIGHT_BLUE_BOLD": ("94", "1"),
    "BRIGHT_MAGENTA_BOLD": ("95", "1"),
    "BRIGHT_CYAN_BOLD": ("96", "1"),
    "BRIGHT_WHITE_BOLD": ("97", "1"),
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

    assert styles[f"BRIGHT_{color}_BOLD"] == styles[f"BRIGHT_{color}"] + BOLD


@pytest.mark.parametrize("color", COLORS)
def test_a_plain_color_is_a_single_code(color: str) -> None:
    assert len(exported_styles()[f"BRIGHT_{color}"].codes) == 1
