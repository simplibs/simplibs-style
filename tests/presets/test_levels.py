import pkgutil
import sys

import pytest
# Outers
import simplibs.style as style_root
import simplibs.style.presets as presets_package
import simplibs.style.presets.levels as folder
from simplibs.style.base_class import StyleDefiner
from simplibs.style.presets import (
    BG_RED,
    BOLD,
    BRIGHT_BLUE,
    BRIGHT_GREEN_BOLD,
    BRIGHT_RED_BOLD,
    BRIGHT_WHITE,
    BRIGHT_YELLOW_BOLD,
    DIM,
)


RESET = "\033[0m"

# Written out by hand
EXPECTED: dict[str, tuple[str, ...]] = {
    "DEBUG": ("2",),
    "INFO": ("94",),
    "SUCCESS": ("92", "1"),
    "WARNING": ("93", "1"),
    "ERROR": ("91", "1"),
    "CRITICAL": ("41", "97", "1"),
}

# The same level written with the presets it is named after
EQUIVALENT: dict[str, StyleDefiner] = {
    "DEBUG": DIM,
    "INFO": BRIGHT_BLUE,
    "SUCCESS": BRIGHT_GREEN_BOLD,
    "WARNING": BRIGHT_YELLOW_BOLD,
    "ERROR": BRIGHT_RED_BOLD,
    "CRITICAL": BG_RED + BRIGHT_WHITE + BOLD,
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


def test_every_level_has_its_equivalent() -> None:
    assert set(EQUIVALENT) == set(EXPECTED)


@pytest.mark.parametrize("name", list(EXPECTED))
def test_every_file_defines_the_style_the_folder_exports(name: str) -> None:
    module = sys.modules[f"{folder.__name__}.{name}"]

    assert getattr(module, name) is exported_styles()[name]


@pytest.mark.parametrize("name", list(EXPECTED))
def test_every_style_is_also_available_from_the_package_and_the_root(name: str) -> None:
    preset = exported_styles()[name]

    assert getattr(presets_package, name) is preset
    assert getattr(style_root, name) is preset


def test_the_levels_can_be_told_apart() -> None:
    sequences = [style.sequence for style in exported_styles().values()]

    assert len(set(sequences)) == len(EXPECTED)


# ----------------------------------------------------------------------
# Each level
# ----------------------------------------------------------------------
@pytest.mark.parametrize("name, codes", list(EXPECTED.items()))
def test_the_level_has_its_codes(name: str, codes: tuple[str, ...]) -> None:
    style = exported_styles()[name]

    assert isinstance(style, StyleDefiner)
    assert style.codes == codes
    assert style.sequence == "\033[" + ";".join(codes) + "m"


@pytest.mark.parametrize("name, codes", list(EXPECTED.items()))
def test_the_level_styles_a_text(name: str, codes: tuple[str, ...]) -> None:
    style = exported_styles()[name]

    assert style("x", use_style=True) == "\033[" + ";".join(codes) + "mx" + RESET
    assert style("x", use_style=False) == "x"


@pytest.mark.parametrize("name", list(EXPECTED))
def test_the_level_equals_the_presets_it_is_named_after(name: str) -> None:
    assert exported_styles()[name] == EQUIVALENT[name]
