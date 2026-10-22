import pytest
# Outers
from simplibs.style.settings import get_styles_enabled
from simplibs.style.settings._classes.constants import STYLES_OVERRIDE
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


@pytest.mark.parametrize("value", [True, False])
def test_without_an_override_the_process_wide_switch_decides(value: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = value

    assert get_styles_enabled() is value


@pytest.mark.parametrize("global_value", [True, False])
@pytest.mark.parametrize("override", [True, False])
def test_an_active_override_wins_over_the_switch(global_value: bool, override: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = global_value
    token = STYLES_OVERRIDE.set(override)
    try:
        assert get_styles_enabled() is override
    finally:
        STYLES_OVERRIDE.reset(token)


@pytest.mark.parametrize("global_value", [True, False])
def test_the_switch_decides_again_once_the_override_ends(global_value: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = global_value
    token = STYLES_OVERRIDE.set(not global_value)
    STYLES_OVERRIDE.reset(token)

    assert get_styles_enabled() is global_value


def test_follows_the_switch_as_it_moves() -> None:
    GLOBAL_STYLES_SWITCH.enabled = True
    assert get_styles_enabled() is True

    GLOBAL_STYLES_SWITCH.enabled = False
    assert get_styles_enabled() is False


def test_an_override_set_to_false_is_not_mistaken_for_no_override() -> None:
    # `False` is an answer; only `None` means "no override"
    GLOBAL_STYLES_SWITCH.enabled = True
    token = STYLES_OVERRIDE.set(False)
    try:
        assert get_styles_enabled() is False
    finally:
        STYLES_OVERRIDE.reset(token)


def test_the_answer_is_a_bool() -> None:
    assert isinstance(get_styles_enabled(), bool)
