import pytest

from mariner.utils import color


def colors():
    return [
        ("36m", color.cyan),
        ("32m", color.green),
        ("31m", color.red),
        ("33m", color.yellow),
    ]


def colors_ids():
    return ["cyan", "green", "red", "yellow"]


@pytest.mark.parametrize("color_code, color_function", colors(), ids=colors_ids())
def test_colors(color_code, color_function):
    # GIVEN a color function
    # WHEN coloring a string
    colored = color_function("")
    # THEN it should contain the color and reset escape sequences
    assert color_code in colored
    assert "0m" in colored


def test_invalid_color():
    # GIVEN an invalid color
    invalid_color = "turquoise"

    # WHEN coloring a string
    # THEN a ValueError should be raised
    with pytest.raises(ValueError):
        color.color("", invalid_color)
