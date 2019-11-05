import pathlib
import shutil

import pytest

from mariner import config


class TestConfig:
    @pytest.fixture(autouse=True, scope="class")
    def tmp_config(self):
        configpath = pathlib.Path(config.Config().configpath)
        tmp = str(configpath.parent / "tmp5643216.yaml")
        try:
            shutil.copy(str(configpath), tmp)
            yield
            shutil.copy(tmp, str(configpath))
        except FileNotFoundError:
            # Running in CI, config does not exists, so we don't have to care about overwriting it
            yield

    def test_show_config(self, run):
        # GIVEN a configuration
        expected = "{'default_tracker': 'linuxtracker',\n 'download_path': '~/Downloads',\n 'results': 50,\n 'timeout': 10}\n"

        # WHEN showing the configuration
        result = run("--config-file", config.Config.default_config, "config", "-s")[0]

        # THEN it should properly show configured options
        assert result == expected

    def test_change_config(self, run):
        # GIVEN a configuration
        expected = "Updated timeout to 100\n"

        # WHEN changing an option
        result = run("config", "timeout", "100")[1]

        # THEN the configuration should change
        assert result == expected

    def test_change_wrong_config(self, run):
        # GIVEN a configuration
        expected = "Wrong configuration option\n"

        # WHEN changing a non-existant option
        result = run("config", "test", "test")[1]

        # THEN an error should be shown
        assert result == expected
