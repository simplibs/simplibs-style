from contextvars import ContextVar
import threading
# Outers
from simplibs.style.settings._classes.constants import STYLES_OVERRIDE


def test_is_a_context_variable() -> None:
    assert isinstance(STYLES_OVERRIDE, ContextVar)
    assert STYLES_OVERRIDE.name == "STYLES_OVERRIDE"


def test_has_no_override_by_default() -> None:
    assert STYLES_OVERRIDE.get() is None


def test_set_and_reset_bring_the_previous_state_back() -> None:
    token = STYLES_OVERRIDE.set(True)
    assert STYLES_OVERRIDE.get() is True

    STYLES_OVERRIDE.reset(token)
    assert STYLES_OVERRIDE.get() is None


def test_nested_sets_unwind_in_order() -> None:
    outer = STYLES_OVERRIDE.set(False)
    inner = STYLES_OVERRIDE.set(True)
    assert STYLES_OVERRIDE.get() is True

    STYLES_OVERRIDE.reset(inner)
    assert STYLES_OVERRIDE.get() is False

    STYLES_OVERRIDE.reset(outer)
    assert STYLES_OVERRIDE.get() is None


def test_a_value_set_in_another_thread_does_not_reach_this_one() -> None:
    def work() -> None:
        STYLES_OVERRIDE.set(True)

    thread = threading.Thread(target=work)
    thread.start()
    thread.join(timeout=5)

    assert STYLES_OVERRIDE.get() is None
