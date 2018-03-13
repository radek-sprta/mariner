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


def test_cyan():
    """String should be colored cyan."""
    assert '36m' in utils.cyan('')
    assert '0m' in utils.cyan('')


def test_red():
    """String should be colored red."""
    assert '31m' in utils.red('')
    assert '0m' in utils.red('')


def test_yellow():
    """String should be colored yellow."""
    assert '33m' in utils.yellow('')
    assert '0m' in utils.yellow('')


def test_magenta():
    """String should be colored magenta."""
    assert '35m' in utils.magenta('')
    assert '0m' in utils.magenta('')


def test_green():
    """String should be colored green."""
    assert '32m' in utils.green('')
    assert '0m' in utils.green('')
