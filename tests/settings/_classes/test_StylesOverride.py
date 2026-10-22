import asyncio
import threading

import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.settings import get_styles_enabled
from simplibs.style.settings._classes import StylesOverride
from simplibs.style.settings._classes.constants import STYLES_OVERRIDE
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


# ----------------------------------------------------------------------
# The with block
# ----------------------------------------------------------------------
@pytest.mark.parametrize("value", [True, False])
def test_sets_the_override_inside_the_block_only(value: bool) -> None:
    assert STYLES_OVERRIDE.get() is None

    with StylesOverride(value):
        assert STYLES_OVERRIDE.get() is value

    assert STYLES_OVERRIDE.get() is None


@pytest.mark.parametrize("global_value", [True, False])
@pytest.mark.parametrize("override", [True, False])
def test_the_override_wins_over_the_process_wide_switch(global_value: bool, override: bool) -> None:
    GLOBAL_STYLES_SWITCH.enabled = global_value

    with StylesOverride(override):
        assert get_styles_enabled() is override

    assert get_styles_enabled() is global_value


def test_enter_returns_nothing_to_bind() -> None:
    with StylesOverride(True) as bound:
        assert bound is None


def test_restores_the_previous_state_after_an_exception() -> None:
    with pytest.raises(RuntimeError):
        with StylesOverride(False):
            raise RuntimeError("boom")

    assert STYLES_OVERRIDE.get() is None


def test_does_not_swallow_the_exception() -> None:
    with pytest.raises(KeyError):
        with StylesOverride(True):
            raise KeyError("lost")


# ----------------------------------------------------------------------
# Nesting and reuse
# ----------------------------------------------------------------------
def test_nested_blocks_unwind_one_by_one() -> None:
    with StylesOverride(False):
        assert STYLES_OVERRIDE.get() is False

        with StylesOverride(True):
            assert STYLES_OVERRIDE.get() is True

            with StylesOverride(False):
                assert STYLES_OVERRIDE.get() is False

            assert STYLES_OVERRIDE.get() is True

        assert STYLES_OVERRIDE.get() is False

    assert STYLES_OVERRIDE.get() is None


def test_one_manager_can_be_used_twice_in_a_row() -> None:
    manager = StylesOverride(False)

    with manager:
        assert STYLES_OVERRIDE.get() is False
    assert STYLES_OVERRIDE.get() is None

    with manager:
        assert STYLES_OVERRIDE.get() is False
    assert STYLES_OVERRIDE.get() is None


def test_one_manager_can_be_entered_inside_itself() -> None:
    manager = StylesOverride(False)

    with manager:
        with manager:
            assert STYLES_OVERRIDE.get() is False
        assert STYLES_OVERRIDE.get() is False

    assert STYLES_OVERRIDE.get() is None


def test_an_inner_override_does_not_outlive_its_block_after_an_exception() -> None:
    with StylesOverride(False):
        with pytest.raises(ValueError):
            with StylesOverride(True):
                raise ValueError("inner")

        assert STYLES_OVERRIDE.get() is False

    assert STYLES_OVERRIDE.get() is None


# ----------------------------------------------------------------------
# The decorator
# ----------------------------------------------------------------------
def test_works_as_a_decorator() -> None:
    @StylesOverride(False)
    def read() -> bool:
        return get_styles_enabled()

    GLOBAL_STYLES_SWITCH.enabled = True

    assert read() is False
    assert get_styles_enabled() is True


def test_a_decorated_function_keeps_its_arguments_and_result() -> None:
    @StylesOverride(True)
    def add(a: int, b: int, *, extra: int = 0) -> int:
        return a + b + extra

    assert add(1, 2, extra=3) == 6


def test_a_decorated_function_can_be_called_again_and_again() -> None:
    @StylesOverride(False)
    def read() -> bool:
        return STYLES_OVERRIDE.get()

    assert [read(), read(), read()] == [False, False, False]
    assert STYLES_OVERRIDE.get() is None


def test_a_decorated_function_can_call_itself() -> None:
    seen: list[bool | None] = []

    @StylesOverride(False)
    def descend(depth: int) -> None:
        seen.append(STYLES_OVERRIDE.get())
        if depth:
            descend(depth - 1)
        seen.append(STYLES_OVERRIDE.get())

    descend(2)

    assert seen == [False] * 6
    assert STYLES_OVERRIDE.get() is None


def test_a_decorated_function_restores_the_state_after_an_exception() -> None:
    @StylesOverride(False)
    def fail() -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        fail()

    assert STYLES_OVERRIDE.get() is None


def test_each_call_of_a_decorated_function_gets_its_own_manager() -> None:
    manager = StylesOverride(True)

    recreated = manager._recreate_cm()

    assert isinstance(recreated, StylesOverride)
    assert recreated is not manager
    assert repr(recreated) == repr(manager)


# ----------------------------------------------------------------------
# Threads and async tasks
# ----------------------------------------------------------------------
def test_an_override_in_one_thread_is_invisible_to_the_others() -> None:
    inside = threading.Event()
    release = threading.Event()
    seen_in_thread: list[bool | None] = []

    def work() -> None:
        with StylesOverride(True):
            seen_in_thread.append(STYLES_OVERRIDE.get())
            inside.set()
            release.wait(timeout=5)

    thread = threading.Thread(target=work)
    thread.start()
    try:
        assert inside.wait(timeout=5)
        assert STYLES_OVERRIDE.get() is None
    finally:
        release.set()
        thread.join(timeout=5)

    assert seen_in_thread == [True]


def test_an_override_in_one_async_task_is_invisible_to_the_others() -> None:
    async def overridden() -> bool | None:
        with StylesOverride(False):
            await asyncio.sleep(0)
            return STYLES_OVERRIDE.get()

    async def plain() -> bool | None:
        await asyncio.sleep(0)
        return STYLES_OVERRIDE.get()

    async def main() -> list[bool | None]:
        return list(await asyncio.gather(overridden(), plain()))

    assert asyncio.run(main()) == [False, None]
    assert STYLES_OVERRIDE.get() is None


# ----------------------------------------------------------------------
# Misuse guard
# ----------------------------------------------------------------------
@pytest.mark.parametrize("value", [True, False])
def test_using_it_as_a_yes_no_value_raises(value: bool) -> None:
    manager = StylesOverride(value)

    with pytest.raises(ParamError) as caught:
        bool(manager)

    assert caught.value.error_name == "STYLE_OVERRIDE_USED_AS_BOOL"


def test_the_condition_form_raises_too() -> None:
    with pytest.raises(ParamError):
        if StylesOverride(True):
            pass

    with pytest.raises(ParamError):
        not StylesOverride(False)


def test_the_error_is_also_a_type_error() -> None:
    with pytest.raises(TypeError):
        bool(StylesOverride(True))


def test_the_misuse_guard_does_not_touch_the_override() -> None:
    with pytest.raises(ParamError):
        bool(StylesOverride(False))

    assert STYLES_OVERRIDE.get() is None


# ----------------------------------------------------------------------
# Representation
# ----------------------------------------------------------------------
@pytest.mark.parametrize("value", [True, False])
def test_repr_shows_the_value(value: bool) -> None:
    assert repr(StylesOverride(value)) == f"StylesOverride({value!r})"
