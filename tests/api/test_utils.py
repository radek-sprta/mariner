import pathlib

import pytest

from mariner import utils


@pytest.fixture(params=["subdir", "subdir2/file.txt"])
def path(tmpdir, request):
    directory = str(tmpdir.mkdir("tmp"))
    return pathlib.Path(directory) / request.param


def test_check_path(path):
    # GIVEN a filesystem path
    # WHEN when checking the path
    result = utils.check_path(path)
    # THEN the directories should exist
    assert result.exists() or result.parent.exists()
    assert isinstance(result, pathlib.Path)


def test_check_str_path(path):
    # GIVEN a string representation of a filesystem path
    path = str(path)
    # WHEN when checking the path
    result = utils.check_path(path)
    # THEN the directories should exist a be Path
    assert result.exists() or result.parent.exists()
    assert isinstance(result, pathlib.Path)


def colors():
    return [
        ("36m", utils.cyan),
        ("32m", utils.green),
        ("31m", utils.red),
        ("33m", utils.yellow),
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
    color = "turquoise"

    # WHEN coloring a string
    # THEN a ValueError should be raised
    with pytest.raises(ValueError):
        utils.color("", color)


def test_parse_number():
    """Returns an integer out of number string."""
    assert utils.parse_number("1,000,000") == 1000000
    assert utils.parse_number("1 000 000") == 1000000
    assert utils.parse_number("-") == 0
