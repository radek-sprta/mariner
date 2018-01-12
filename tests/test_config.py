import atexit
import pathlib

import pytest

from .context import mariner
from mariner import config


@pytest.fixture
def configuration(monkeypatch):
    """Mock configuration."""
    monkeypatch.setenv('XDG_CONFIG_HOME', 'tests/data')
    monkeypatch.setattr(atexit, 'register', lambda *args: None)
    return config.Config()


class TestConfig:
    """Test config.py."""

    def test_default_directory(self, configuration):
        assert isinstance(configuration.default_directory, str)

    def test_xdg_config_path(self, configuration):
        test_path = pathlib.Path('tests/data/config.yaml')
        assert configuration.configpath == test_path
        assert configuration.configpath.exists()

    def test_no_xdg_config_path(self, monkeypatch):
        monkeypatch.delenv('XDG_CONFIG_HOME', raising=False)
        configuration = config.Config()
        test_path = pathlib.Path('~/.config/mariner/config.yaml').expanduser()
        assert configuration.configpath == test_path
        assert configuration.configpath.parent.exists()

    def test_load(self, configuration):
        assert configuration['download_path'] == '~/Downloads'

    def test_roundabout(self, tmpdir, configuration, monkeypatch):
        directory = tmpdir.mkdir('test')
        monkeypatch.setenv('XDG_CONFIG_HOME', directory)
        configuration.save()
        assert configuration.configpath.exists()
        configuration.load()
        assert configuration['download_path'] == '~/Downloads'
        assert configuration['default_tracker'] == 'distrowatch'
