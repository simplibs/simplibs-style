import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.base_class import StyleDefiner
from simplibs.style.settings import set_styles_enabled, styles_disabled, styles_enabled


RED = StyleDefiner("91")
GREEN = StyleDefiner("32")
BOLD = StyleDefiner("1")
RESET = "\033[0m"


# ----------------------------------------------------------------------
# Construction: what goes in
# ----------------------------------------------------------------------
def test_one_code() -> None:
    style = StyleDefiner("91")

    assert style.codes == ("91",)
    assert style.sequence == "\033[91m"


def test_several_codes_are_joined_by_semicolons() -> None:
    style = StyleDefiner("91", "1")

    assert style.codes == ("91", "1")
    assert style.sequence == "\033[91;1m"


def test_a_multi_part_code_stays_one_code() -> None:
    style = StyleDefiner("38;5;208")

    assert style.codes == ("38;5;208",)
    assert style.sequence == "\033[38;5;208m"


def test_every_spelling_of_a_code_gives_the_same_style() -> None:
    assert StyleDefiner("91").codes == StyleDefiner("91m").codes == StyleDefiner("\033[91m").codes == ("91",)


def test_spellings_can_be_mixed_in_one_call() -> None:
    style = StyleDefiner("91m", "\033[1m", "4")

    assert style.codes == ("91", "1", "4")
    assert style.sequence == "\033[91;1;4m"


def test_a_ready_style_brings_its_codes() -> None:
    style = StyleDefiner(RED, "1")

    assert style.codes == ("91", "1")


def test_several_ready_styles_are_joined_in_order() -> None:
    style = StyleDefiner(RED, BOLD, GREEN)

    assert style.codes == ("91", "1", "32")
    assert style.sequence == "\033[91;1;32m"


def test_a_style_made_from_one_style_is_a_new_equal_object() -> None:
    copy = StyleDefiner(RED)

    assert copy is not RED
    assert copy == RED


def test_repeated_codes_are_kept() -> None:
    assert StyleDefiner("1", "1").codes == ("1", "1")


def test_the_style_it_is_built_from_stays_as_it_was() -> None:
    StyleDefiner(RED, "1")

    assert RED.codes == ("91",)


# ----------------------------------------------------------------------
# Construction: what is refused
# ----------------------------------------------------------------------
def test_no_codes_at_all_is_refused() -> None:
    with pytest.raises(ParamError) as caught:
        StyleDefiner()

    assert caught.value.error_name == "STYLE_NO_CODES"
    assert isinstance(caught.value, ValueError)


@pytest.mark.parametrize(
    "entry, error_name",
    [
        (91, "STYLE_CODE_NOT_TEXT"),
        (None, "STYLE_CODE_NOT_TEXT"),
        ("", "STYLE_EMPTY_CODE"),
        ("m", "STYLE_EMPTY_CODE"),
        ("\033[91", "STYLE_INVALID_ANSI_FORMAT"),
        ("red", "STYLE_INVALID_CODE"),
        ("9;", "STYLE_INVALID_CODE"),
    ],
)
def test_a_bad_code_is_refused_with_the_error_of_its_kind(entry: object, error_name: str) -> None:
    with pytest.raises(ParamError) as caught:
        StyleDefiner(entry)  # type: ignore[arg-type]

    assert caught.value.error_name == error_name


def test_one_bad_code_among_good_ones_spoils_the_whole_style() -> None:
    with pytest.raises(ParamError) as caught:
        StyleDefiner("91", "oops", "1")

    assert caught.value.error_name == "STYLE_INVALID_CODE"


# ----------------------------------------------------------------------
# Read-only data
# ----------------------------------------------------------------------
def test_codes_is_a_tuple_of_strings() -> None:
    assert isinstance(RED.codes, tuple)
    assert all(type(code) is str for code in RED.codes)


def test_codes_cannot_be_replaced() -> None:
    with pytest.raises(AttributeError):
        RED.codes = ("1",)  # type: ignore[misc]


def test_sequence_cannot_be_replaced() -> None:
    with pytest.raises(AttributeError):
        RED.sequence = "x"  # type: ignore[misc]


def test_has_no_room_for_other_attributes() -> None:
    style = StyleDefiner("91")

    with pytest.raises(AttributeError):
        style.other = 1  # type: ignore[attr-defined]

    assert not hasattr(style, "__dict__")


# ----------------------------------------------------------------------
# Applying a style
# ----------------------------------------------------------------------
def test_styles_the_text_when_forced_on() -> None:
    assert RED("hello", use_style=True) == f"\033[91mhello{RESET}"


def test_a_combined_style_writes_one_sequence() -> None:
    assert StyleDefiner("91", "1")("hi", use_style=True) == f"\033[91;1mhi{RESET}"


def test_returns_the_text_unchanged_when_forced_off() -> None:
    assert RED("hello", use_style=False) == "hello"


@pytest.mark.parametrize("use_style", [True, False])
def test_an_empty_text_stays_empty(use_style: bool) -> None:
    assert RED("", use_style=use_style) == ""


def test_without_use_style_the_process_wide_switch_decides() -> None:
    set_styles_enabled(True)
    assert RED("x") == f"\033[91mx{RESET}"

    set_styles_enabled(False)
    assert RED("x") == "x"


def test_without_use_style_a_scoped_override_decides() -> None:
    set_styles_enabled(True)
    with styles_disabled():
        assert RED("x") == "x"

    set_styles_enabled(False)
    with styles_enabled():
        assert RED("x") == f"\033[91mx{RESET}"


def test_use_style_wins_over_everything_else() -> None:
    set_styles_enabled(False)
    with styles_disabled():
        assert RED("x", use_style=True) == f"\033[91mx{RESET}"

    set_styles_enabled(True)
    with styles_enabled():
        assert RED("x", use_style=False) == "x"


def test_use_style_none_means_ask_the_settings() -> None:
    set_styles_enabled(True)

    assert RED("x", use_style=None) == f"\033[91mx{RESET}"


def test_use_style_can_only_be_given_by_name() -> None:
    with pytest.raises(TypeError):
        RED("x", True)  # type: ignore[misc]


@pytest.mark.parametrize("use_style", [1, 0, "yes", "", [], 1.0])
def test_use_style_that_is_not_a_bool_is_refused(use_style: object) -> None:
    with pytest.raises(ParamError) as caught:
        RED("x", use_style=use_style)  # type: ignore[arg-type]

    assert caught.value.error_name == "STYLE_USE_STYLE_NOT_BOOL"
    assert isinstance(caught.value, TypeError)


@pytest.mark.parametrize("use_style", [True, False])
def test_a_refused_use_style_is_refused_whatever_the_text(use_style: bool) -> None:
    with pytest.raises(ParamError):
        RED("", use_style=1)  # type: ignore[arg-type]


class Printable:
    def __str__(self) -> str:
        return "shown"


@pytest.mark.parametrize(
    "text, as_text",
    [
        (42, "42"),
        (3.5, "3.5"),
        (None, "None"),
        (True, "True"),
        ([1, 2], "[1, 2]"),
        (Printable(), "shown"),
    ],
)
def test_anything_that_is_not_text_is_converted_first(text: object, as_text: str) -> None:
    assert RED(text, use_style=True) == f"\033[91m{as_text}{RESET}"
    assert RED(text, use_style=False) == as_text


def test_the_result_is_always_a_string() -> None:
    assert type(RED(42, use_style=False)) is str
    assert type(RED(42, use_style=True)) is str


def test_an_inner_style_does_not_cut_the_outer_one_short() -> None:
    inner = GREEN("g", use_style=True)

    result = StyleDefiner(RED, BOLD)(f"x {inner} y", use_style=True)

    assert result == f"\033[91;1mx \033[32mg{RESET}\033[91;1m y{RESET}"


def test_one_style_can_be_used_again_and_again() -> None:
    assert RED("a", use_style=True) == RED("a", use_style=True)
    assert RED("b", use_style=True) == f"\033[91mb{RESET}"


# ----------------------------------------------------------------------
# Composition
# ----------------------------------------------------------------------
def test_plus_joins_two_styles() -> None:
    combined = RED + BOLD

    assert isinstance(combined, StyleDefiner)
    assert combined.codes == ("91", "1")
    assert combined.sequence == "\033[91;1m"


def test_plus_leaves_both_sides_as_they_were() -> None:
    RED + BOLD

    assert RED.codes == ("91",)
    assert BOLD.codes == ("1",)


def test_plus_gives_a_new_object() -> None:
    combined = RED + BOLD

    assert combined is not RED
    assert combined is not BOLD


def test_the_order_of_the_sum_is_the_order_of_the_codes() -> None:
    assert (RED + BOLD).codes == ("91", "1")
    assert (BOLD + RED).codes == ("1", "91")


def test_grouping_does_not_matter() -> None:
    assert ((RED + BOLD) + GREEN) == (RED + (BOLD + GREEN))
    assert ((RED + BOLD) + GREEN).codes == ("91", "1", "32")


def test_a_style_can_be_added_to_itself() -> None:
    assert (BOLD + BOLD).codes == ("1", "1")


def test_sum_joins_a_whole_list() -> None:
    assert sum([RED, BOLD, GREEN]).codes == ("91", "1", "32")


def test_sum_of_one_style_is_that_style() -> None:
    assert sum([RED]) is RED


def test_zero_plus_a_style_is_the_style() -> None:
    assert 0 + RED is RED


@pytest.mark.parametrize("other", [1, -1, 0.0, False, True, "1", "\033[1m", None, ["1"], ("1",)])
def test_only_a_style_can_be_added_to_a_style(other: object) -> None:
    with pytest.raises(TypeError):
        RED + other  # type: ignore[operator]

    with pytest.raises(TypeError):
        other + RED  # type: ignore[operator]


def test_add_hands_back_when_it_does_not_understand() -> None:
    assert RED.__add__("1") is NotImplemented
    assert RED.__radd__("1") is NotImplemented


# ----------------------------------------------------------------------
# Identity
# ----------------------------------------------------------------------
def test_styles_with_the_same_codes_are_equal() -> None:
    assert StyleDefiner("91", "1") == StyleDefiner("91", "1")


def test_equality_does_not_depend_on_how_a_code_was_written() -> None:
    assert StyleDefiner("91") == StyleDefiner("91m") == StyleDefiner("\033[91m")


def test_equality_follows_the_sequence_not_the_grouping_of_codes() -> None:
    assert StyleDefiner("1", "31") == StyleDefiner("1;31")


def test_the_order_of_codes_matters() -> None:
    assert StyleDefiner("91", "1") != StyleDefiner("1", "91")


def test_different_styles_are_not_equal() -> None:
    assert RED != GREEN


@pytest.mark.parametrize("other", ["\033[91m", "91", ("91",), 91, None])
def test_a_style_is_not_equal_to_anything_else(other: object) -> None:
    assert (RED == other) is False
    assert (RED != other) is True


def test_equal_styles_have_the_same_hash() -> None:
    assert hash(StyleDefiner("91")) == hash(StyleDefiner("\033[91m"))


def test_styles_work_as_set_members_and_dictionary_keys() -> None:
    assert len({StyleDefiner("91"), StyleDefiner("91m"), StyleDefiner("32")}) == 2

    names = {RED: "red", GREEN: "green"}
    assert names[StyleDefiner("\033[91m")] == "red"


# ----------------------------------------------------------------------
# Representation
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "style, expected",
    [
        (StyleDefiner("91"), "StyleDefiner('91')"),
        (StyleDefiner("91", "1"), "StyleDefiner('91', '1')"),
        (StyleDefiner("38;5;208"), "StyleDefiner('38;5;208')"),
        (StyleDefiner(RED, BOLD), "StyleDefiner('91', '1')"),
    ],
)
def test_repr_lists_the_bare_codes(style: StyleDefiner, expected: str) -> None:
    assert repr(style) == expected


@pytest.mark.parametrize("style", [RED, RED + BOLD, StyleDefiner("38;2;255;136;0")])
def test_repr_can_be_evaluated_back_into_an_equal_style(style: StyleDefiner) -> None:
    assert eval(repr(style), {"StyleDefiner": StyleDefiner}) == style
