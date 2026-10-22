import pytest
# Outers
from simplibs.style.settings._helpers._is_env_flag_set import _is_env_flag_set


NAME = "SIMPLIBS_STYLE_TEST_FLAG"


@pytest.fixture(autouse=True)
def unset_test_flag(monkeypatch) -> None:
    monkeypatch.delenv(NAME, raising=False)


@pytest.mark.parametrize("value", ["1", "yes", "true", "anything", " x ", "0", "false"])
def test_any_non_blank_value_counts_as_set(monkeypatch, value: str) -> None:
    # Even "0" and "false": the presence of the variable is what counts
    monkeypatch.setenv(NAME, value)

    assert _is_env_flag_set(NAME) is True


@pytest.mark.parametrize("value", ["", " ", "   ", "\t", "\n", " \t\n "])
def test_an_empty_or_blank_value_counts_as_not_set(monkeypatch, value: str) -> None:
    monkeypatch.setenv(NAME, value)

    assert _is_env_flag_set(NAME) is False


def test_a_missing_variable_is_not_set() -> None:
    assert _is_env_flag_set(NAME) is False


def test_only_the_named_variable_is_read(monkeypatch) -> None:
    monkeypatch.setenv(NAME + "_OTHER", "1")

    assert _is_env_flag_set(NAME) is False
