import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError
from simplibs.style.colors._validations import raise_color_hex_invalid_error


_EXPECTED = "Six or three hex digits, with or without '#': '#ff8800', 'ff8800', '#f80'."
_HOW_TO_FIX = (
    "Use only the digits 0-9 and the letters a-f.",
    "Remove spaces, a '0x' prefix and any alpha channel.",
)


@pytest.mark.parametrize(
    "value",
    ["", "#", "#ff88", "#gg8800", "#ff8800ff", "0xff8800", "ff 88 00", "red"],
)
def test_raise_color_hex_invalid_error_text_is_a_value_error(subtests, value) -> None:
    """Verify a text of the wrong shape is a ValueError with its own problem."""

    assert_exception_function(
        subtests,
        raise_color_hex_invalid_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="STYLE_COLOR_HEX_INVALID",
        label="hex color",
        expected=_EXPECTED,
        value=value,
        problem="The text is not a hex color.",
        how_to_fix=_HOW_TO_FIX,
        exception=ValueError,
        verbose=False,
    )


@pytest.mark.parametrize("value", [255, 0xFF8800, 1.5, None, True, b"ff8800", ["ff", "88", "00"], (255, 136, 0)])
def test_raise_color_hex_invalid_error_other_type_is_a_type_error(subtests, value) -> None:
    """Verify a value that is not text is a TypeError with its own problem."""

    assert_exception_function(
        subtests,
        raise_color_hex_invalid_error,
        invalid_params=(value,),
        exception_type=ParamError,
        error_name="STYLE_COLOR_HEX_INVALID",
        label="hex color",
        expected=_EXPECTED,
        value=value,
        problem="A hex color is written as text.",
        how_to_fix=_HOW_TO_FIX,
        exception=TypeError,
        verbose=False,
    )
