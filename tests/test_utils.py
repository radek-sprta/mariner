import pathlib

import pytest

from .context import mariner
from mariner import utils


def test_check_path(tmpdir):
    directory = str(tmpdir.mkdir('tmp'))
    path = pathlib.Path(directory) / 'subdir'
    path2 = pathlib.Path(directory) / 'subdir2' / 'file.txt'
    utils.check_path(path)
    utils.check_path(path2)
    assert path.exists()
    assert path2.parent.exists()
