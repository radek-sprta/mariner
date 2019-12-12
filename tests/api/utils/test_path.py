import pathlib

import pytest

from mariner.utils import path


@pytest.fixture(params=["subdir", "subdir2/file.txt"])
def test_path(tmpdir, request):
    directory = str(tmpdir.mkdir("tmp"))
    return pathlib.Path(directory) / request.param


def test_check(test_path):
    # GIVEN a filesystem path
    # WHEN when checking the path
    result = path.check(test_path)
    # THEN the directories should exist
    assert result.exists() or result.parent.exists()
    assert isinstance(result, pathlib.Path)


def test_check_str_path(test_path):
    # GIVEN a string representation of a filesystem path
    test_path = str(test_path)
    # WHEN when checking the path
    result = path.check(test_path)
    # THEN the directories should exist a be Path
    assert result.exists() or result.parent.exists()
    assert isinstance(result, pathlib.Path)
