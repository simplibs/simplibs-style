import pytest
# Outers
from simplibs.style.settings._classes import StylesSwitch


@pytest.mark.parametrize("value", [True, False])
def test_keeps_the_starting_position(value: bool) -> None:
    assert StylesSwitch(value).enabled is value


@pytest.mark.parametrize("start", [True, False])
def test_can_be_moved(start: bool) -> None:
    switch = StylesSwitch(start)

    switch.enabled = not start

    assert switch.enabled is (not start)


def test_two_switches_are_independent() -> None:
    first = StylesSwitch(True)
    second = StylesSwitch(True)

    first.enabled = False

    assert second.enabled is True


def test_has_no_room_for_other_attributes() -> None:
    switch = StylesSwitch(True)

    with pytest.raises(AttributeError):
        switch.other = 1  # type: ignore[attr-defined]

    assert not hasattr(switch, "__dict__")


@pytest.mark.parametrize("value", [True, False])
def test_repr_shows_the_position(value: bool) -> None:
    assert repr(StylesSwitch(value)) == f"StylesSwitch(enabled={value!r})"


def test_repr_follows_the_current_position() -> None:
    switch = StylesSwitch(True)
    switch.enabled = False

    assert repr(switch) == "StylesSwitch(enabled=False)"
