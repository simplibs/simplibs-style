import pytest
# Outers
from simplibs.exception import ParamError
from simplibs.style.colors._helpers import require_color_value


class Level(int):
    """An int subclass that is not a bool."""


@pytest.mark.parametrize("value", [0, 1, 16, 127, 128, 208, 254, 255])
def test_accepts_every_integer_of_one_byte(value: int) -> None:
    assert require_color_value(value, "n") is None


def test_accepts_an_int_subclass() -> None:
    assert require_color_value(Level(200), "n") is None


@pytest.mark.parametrize("value", [-1, 256, 300, -255, 1000, 10**10, -(10**10)])
def test_refuses_an_integer_outside_one_byte(value: int) -> None:
    with pytest.raises(ParamError) as caught:
        require_color_value(value, "n")

    assert caught.value.error_name == "STYLE_COLOR_OUT_OF_RANGE"
    assert isinstance(caught.value, ValueError)


@pytest.mark.parametrize(
    "value",
    [1.0, 255.0, 0.5, "208", "", None, True, False, [], (1,), b"1", 1 + 0j, object()],
)
def test_refuses_everything_that_is_not_an_integer(value: object) -> None:
    with pytest.raises(ParamError) as caught:
        require_color_value(value, "n")

    assert caught.value.error_name == "STYLE_COLOR_NOT_INT"
    assert isinstance(caught.value, TypeError)


@pytest.mark.parametrize("value", [True, False])
def test_a_bool_is_not_a_number_here_even_though_python_thinks_so(value: bool) -> None:
    # True is 1 and False is 0, both inside the range — yet neither is accepted
    with pytest.raises(ParamError) as caught:
        require_color_value(value, "n")

    assert caught.value.error_name == "STYLE_COLOR_NOT_INT"


def test_a_wrong_kind_is_reported_before_a_wrong_size() -> None:
    # 1000.5 is both: it is refused for its type, not for its size
    with pytest.raises(ParamError) as caught:
        require_color_value(1000.5, "n")

    assert caught.value.error_name == "STYLE_COLOR_NOT_INT"


@pytest.mark.parametrize("label", ["n", "r", "g", "b"])
def test_the_label_reaches_the_error_of_a_wrong_kind(label: str) -> None:
    with pytest.raises(ParamError) as caught:
        require_color_value("x", label)

    assert caught.value.label == label


@pytest.mark.parametrize("label", ["n", "r", "g", "b"])
def test_the_label_reaches_the_error_of_a_wrong_size(label: str) -> None:
    with pytest.raises(ParamError) as caught:
        require_color_value(256, label)

    assert caught.value.label == label
