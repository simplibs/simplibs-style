import pytest
# Outers
from simplibs.style.base_class._helpers import apply_style


RED = "\033[91m"
GREEN = "\033[32m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ----------------------------------------------------------------------
# The plain case
# ----------------------------------------------------------------------
def test_wraps_the_text_in_the_sequence_and_a_reset() -> None:
    assert apply_style(RED, "hello") == "\033[91mhello\033[0m"


def test_an_empty_text_stays_empty() -> None:
    assert apply_style(RED, "") == ""


@pytest.mark.parametrize("text", [" ", "\n", "0", "m"])
def test_a_text_that_only_looks_empty_is_still_styled(text: str) -> None:
    assert apply_style(RED, text) == f"{RED}{text}{RESET}"


def test_the_sequence_is_used_exactly_as_given() -> None:
    assert apply_style("<", "x") == "<x\033[0m"


def test_keeps_the_text_untouched_otherwise() -> None:
    text = "řádek 1\nřádek 2\t✓ \\ \"quoted\""

    assert apply_style(RED, text) == f"{RED}{text}{RESET}"


def test_the_result_is_a_string() -> None:
    assert type(apply_style(RED, "x")) is str


# ----------------------------------------------------------------------
# A text that already holds styles
# ----------------------------------------------------------------------
def test_the_style_continues_after_an_inner_styled_part() -> None:
    text = f"x {GREEN}green{RESET} y"

    assert apply_style(RED, text) == f"{RED}x {GREEN}green{RESET}{RED} y{RESET}"


@pytest.mark.parametrize("inner_reset", ["\033[0m", "\033[00m", "\033[m"])
def test_every_spelling_of_a_lone_reset_is_followed_by_the_sequence(inner_reset: str) -> None:
    text = f"a{inner_reset}b"

    assert apply_style(RED, text) == f"{RED}a{inner_reset}{RED}b{RESET}"


def test_every_inner_reset_is_followed_by_the_sequence() -> None:
    text = f"{GREEN}a{RESET} {GREEN}b{RESET} c"

    expected = f"{RED}{GREEN}a{RESET}{RED} {GREEN}b{RESET}{RED} c{RESET}"
    assert apply_style(RED, text) == expected


def test_a_reset_at_the_very_end_is_followed_by_the_sequence_too() -> None:
    text = f"{GREEN}tail{RESET}"

    assert apply_style(RED, text) == f"{RED}{GREEN}tail{RESET}{RED}{RESET}"


def test_a_combined_reset_is_not_touched() -> None:
    text = "a\033[0;1mb"

    assert apply_style(RED, text) == f"{RED}a\033[0;1mb{RESET}"


def test_other_inner_sequences_are_not_touched() -> None:
    text = f"a{BOLD}b\033[39mc"

    assert apply_style(RED, text) == f"{RED}a{BOLD}b\033[39mc{RESET}"


def test_a_text_that_mentions_a_reset_without_the_escape_is_not_touched() -> None:
    text = "type [0m to reset"

    assert apply_style(RED, text) == f"{RED}{text}{RESET}"


def test_styling_twice_keeps_both_styles_alive() -> None:
    inner = apply_style(GREEN, "mid")
    outer = apply_style(RED, f"a {inner} b")

    assert outer == f"{RED}a {GREEN}mid{RESET}{RED} b{RESET}"
