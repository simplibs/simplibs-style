import pytest
# Outers
from simplibs.style.settings._constants import GLOBAL_STYLES_SWITCH


ENVIRONMENT_NAMES = ("NO_COLOR", "FORCE_COLOR", "TERM")


@pytest.fixture(autouse=True)
def restore_global_styles_switch():
    """Give every test the process-wide switch as it found it.

    Tests may move the switch freely; whatever they do, the next test
    starts from the original position.
    """

    saved = GLOBAL_STYLES_SWITCH.enabled
    yield
    GLOBAL_STYLES_SWITCH.enabled = saved


@pytest.fixture
def clean_environment(monkeypatch):
    """Remove every environment variable that influences the styling default.

    Afterwards a test sets only what it needs; `monkeypatch` puts the real
    environment back when the test ends.
    """

    for name in ENVIRONMENT_NAMES:
        monkeypatch.delenv(name, raising=False)
