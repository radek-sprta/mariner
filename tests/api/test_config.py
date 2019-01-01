import atexit
import pathlib

import pytest

from mariner import config


@pytest.fixture
def configuration(monkeypatch):
    """Mock configuration."""
    monkeypatch.setenv("XDG_CONFIG_HOME", "tests/api/data")
    monkeypatch.setattr(atexit, "register", lambda *args: None)
    return config.Config()


class TestConfig:
    """Test config.py."""

    def test_default_directory(self, configuration):
        assert isinstance(configuration.default_directory, str)

    def test_xdg_config_path(self, configuration):
        # GIVEN configuration with XDG_CONFIG_HOME set

        # WHEN checking the config path
        test_path = pathlib.Path("tests/api/data/config.yaml")

        # THEN it should be in the XDG_CONFIG_HOME
        assert configuration.configpath.exists()
        assert configuration.configpath == test_path

    def test_no_xdg_config_path(self, monkeypatch):
        # GIVEN a configuration with XDG_CONFIG_HOME not set
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        configuration = config.Config()

        # WHEN checking the config path
        test_path = pathlib.Path(configuration.default_directory).expanduser() / "config.yaml"

        # THEN it should use the default_directory
        assert configuration.configpath.parent.exists()
        assert configuration.configpath == test_path

    def test_load(self, configuration):
        # GIVEN a configuration
        # WHEN loading it
        # THEN it should load the values
        assert configuration["download_path"] == "~/Downloads"
        assert configuration["default_tracker"] == "distrowatch"

    @pytest.mark.smoke
    def test_roundabout(self, tmpdir, configuration, monkeypatch):
        # GIVEN a configuration
        directory = str(tmpdir.mkdir("test"))
        monkeypatch.setenv("XDG_CONFIG_HOME", directory)
        download_path = configuration["download_path"]
        default_tracker = configuration["default_tracker"]
        configuration["test"] = "test"

        # WHEN saving it and loading it
        configuration.save()
        configuration.load()

        # THEN it should have the same values as before loading
        assert configuration["download_path"] == download_path
        assert configuration["default_tracker"] == default_tracker
        assert configuration["test"] == "test"

    def test_access_nonexistant_attribute(self, configuration):
        # GIVEN a configuration
        # WHEN trying to access a non-existant attribute
        # THEN an exception should be raised
        with pytest.raises(KeyError):
            configuration["invalid"]

    def test_delete_attribute(self, configuration):
        # GIVEN a configuration with added attribute
        configuration["test"] = "test"
        assert "test" in configuration

        # WHEN deleting the attribute
        del configuration["test"]

        # THEN it should not be in the configuration
        assert "test" not in configuration

    def test_configuration_len(self, configuration):
        # GIVEN a configuration with 4 items
        # WHEN checking the length
        # THEN it should return 4
        assert len(configuration) == 4

    def test_iteration(self, configuration):
        # GIVEN a configuration
        # WHEN iterating through it
        count = 0
        for key, value in configuration.items():

            # THEN it should return all the keys and values
            assert configuration[key] == value
            count += 1
        assert count == len(configuration)
