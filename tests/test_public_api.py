import inspect
from pathlib import Path
from types import ModuleType

import pytest
# Outers
import simplibs.style as root
import simplibs.style.base_class as base_class_package
import simplibs.style.colors as colors_package
import simplibs.style.presets as presets_package
import simplibs.style.settings as settings_package
import simplibs.style.presets.attributes as attributes_folder
import simplibs.style.presets.background_colors as background_colors_folder
import simplibs.style.presets.bright_background_colors as bright_background_colors_folder
import simplibs.style.presets.bright_colors as bright_colors_folder
import simplibs.style.presets.levels as levels_folder
import simplibs.style.presets.standard_colors as standard_colors_folder
from simplibs.style import StyleDefiner


# The public face of the library, written out by hand
CORE = ["StyleDefiner"]

COLORS = ["color_256", "color_rgb", "color_hex"]

SETTINGS = [
    "get_styles_enabled",
    "set_styles_enabled",
    "reset_styles_enabled",
    "styles_disabled",
    "styles_enabled",
]

ATTRIBUTES = ["BOLD", "DIM", "ITALIC", "UNDERLINE", "BLINK", "REVERSE", "HIDDEN", "STRIKETHROUGH"]

STANDARD_COLORS = [
    "BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE",
    "BLACK_BOLD", "RED_BOLD", "GREEN_BOLD", "YELLOW_BOLD",
    "BLUE_BOLD", "MAGENTA_BOLD", "CYAN_BOLD", "WHITE_BOLD",
]

BRIGHT_COLORS = [
    "BRIGHT_BLACK", "BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW",
    "BRIGHT_BLUE", "BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_WHITE",
    "BRIGHT_BLACK_BOLD", "BRIGHT_RED_BOLD", "BRIGHT_GREEN_BOLD", "BRIGHT_YELLOW_BOLD",
    "BRIGHT_BLUE_BOLD", "BRIGHT_MAGENTA_BOLD", "BRIGHT_CYAN_BOLD", "BRIGHT_WHITE_BOLD",
]

BACKGROUNDS = [
    "BG_BLACK", "BG_RED", "BG_GREEN", "BG_YELLOW",
    "BG_BLUE", "BG_MAGENTA", "BG_CYAN", "BG_WHITE",
]

BRIGHT_BACKGROUNDS = [
    "BG_BRIGHT_BLACK", "BG_BRIGHT_RED", "BG_BRIGHT_GREEN", "BG_BRIGHT_YELLOW",
    "BG_BRIGHT_BLUE", "BG_BRIGHT_MAGENTA", "BG_BRIGHT_CYAN", "BG_BRIGHT_WHITE",
]

LEVELS = ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]

PRESETS = (
    ATTRIBUTES
    + STANDARD_COLORS
    + BRIGHT_COLORS
    + BACKGROUNDS
    + BRIGHT_BACKGROUNDS
    + LEVELS
)

EVERYTHING = CORE + COLORS + SETTINGS + PRESETS

FOLDERS = [
    attributes_folder,
    standard_colors_folder,
    bright_colors_folder,
    background_colors_folder,
    bright_background_colors_folder,
    levels_folder,
]


# ----------------------------------------------------------------------
# The list of public names
# ----------------------------------------------------------------------
def test_all_lists_exactly_the_public_names() -> None:
    assert set(root.__all__) == set(EVERYTHING)


def test_all_has_no_duplicates() -> None:
    assert len(root.__all__) == len(set(root.__all__))


def test_the_expected_names_have_no_duplicates() -> None:
    assert len(EVERYTHING) == len(set(EVERYTHING))


def test_every_listed_name_can_be_read_from_the_root() -> None:
    for name in root.__all__:
        assert hasattr(root, name), name


def test_nothing_public_is_missing_from_all() -> None:
    public = {
        name
        for name, value in vars(root).items()
        if not name.startswith("_") and not isinstance(value, ModuleType)
    }

    assert public == set(root.__all__)


def test_star_import_brings_exactly_the_listed_names() -> None:
    namespace: dict[str, object] = {}
    exec("from simplibs.style import *", namespace)
    namespace.pop("__builtins__")

    assert set(namespace) == set(root.__all__)


# ----------------------------------------------------------------------
# What each name is
# ----------------------------------------------------------------------
def test_the_style_class_is_a_class() -> None:
    assert inspect.isclass(root.StyleDefiner)


@pytest.mark.parametrize("name", COLORS + SETTINGS)
def test_the_builders_and_settings_are_functions(name: str) -> None:
    assert inspect.isfunction(getattr(root, name))


@pytest.mark.parametrize("name", PRESETS)
def test_every_preset_is_a_style(name: str) -> None:
    assert isinstance(getattr(root, name), StyleDefiner)


# ----------------------------------------------------------------------
# The root hands out the very objects of the sub-packages
# ----------------------------------------------------------------------
def test_the_style_class_is_the_one_of_the_base_class_package() -> None:
    assert root.StyleDefiner is base_class_package.StyleDefiner


@pytest.mark.parametrize("name", COLORS)
def test_a_builder_is_the_one_of_the_colors_package(name: str) -> None:
    assert getattr(root, name) is getattr(colors_package, name)


@pytest.mark.parametrize("name", SETTINGS)
def test_a_setting_is_the_one_of_the_settings_package(name: str) -> None:
    assert getattr(root, name) is getattr(settings_package, name)


@pytest.mark.parametrize("name", PRESETS)
def test_a_preset_is_the_one_of_the_presets_package(name: str) -> None:
    assert getattr(root, name) is getattr(presets_package, name)


# ----------------------------------------------------------------------
# The presets package
# ----------------------------------------------------------------------
def test_the_presets_package_lists_exactly_the_presets() -> None:
    assert set(presets_package.__all__) == set(PRESETS)
    assert len(presets_package.__all__) == len(set(presets_package.__all__))


def test_the_presets_package_lists_everything_its_folders_define() -> None:
    defined = {
        name
        for folder in FOLDERS
        for name, value in vars(folder).items()
        if isinstance(value, StyleDefiner)
    }

    assert defined == set(presets_package.__all__)


def test_the_presets_package_has_sixty_two_presets() -> None:
    assert len(PRESETS) == 62


# ----------------------------------------------------------------------
# The library as a user meets it
# ----------------------------------------------------------------------
def test_a_preset_styles_a_text() -> None:
    assert root.RED("x", use_style=True) == "\033[31mx\033[0m"


def test_presets_combine_with_plus() -> None:
    assert (root.RED + root.BOLD)("x", use_style=True) == "\033[31;1mx\033[0m"


def test_a_level_styles_a_text() -> None:
    assert root.ERROR("x", use_style=True) == "\033[91;1mx\033[0m"


def test_a_color_builder_styles_a_text() -> None:
    assert root.color_rgb(255, 136, 0)("x", use_style=True) == "\033[38;2;255;136;0mx\033[0m"


def test_the_package_ships_its_type_marker() -> None:
    assert (Path(root.__file__).parent / "py.typed").is_file()
