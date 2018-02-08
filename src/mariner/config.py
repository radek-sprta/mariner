"""Handle application configuration."""
import atexit
import collections
import logging
import os
import pathlib
from typing import Dict, List, Union

import pkg_resources
import ruamel.yaml

from mariner import utils

Value = Union[str, int, Dict, List]


class Config(collections.abc.MutableMapping):
    """Class to hold config settings using yaml. Behaves like a dictionary."""
    default_directory = '~/.config/mariner/'
    default_config = pkg_resources.resource_filename(
        __name__, 'config/config.yaml')
    log = logging.getLogger(__name__)

    def __init__(self, _parent: 'Config' = None,
                 _config: Union['Config', Dict] = None) -> None:
        self._yaml = ruamel.yaml.YAML()
        self._parent = _parent

        if not self._parent:
            self._config = self.load()
        else:
            self._config = _config

        # Save the config file on exit
        atexit.register(self.save)

    @property
    def configpath(self) -> pathlib.Path:
        """Create configuration file if necessary and return the path.

        Returns:
            Path to configuration file.
        """
        directory = os.getenv('XDG_CONFIG_HOME', self.default_directory)
        directory = utils.check_path(directory)
        path = pathlib.Path(directory, 'config.yaml')
        self.log.debug('directory=%s path=%s', directory, path)
        return path

    def load(self) -> Dict:
        """Load configuration saved in given path.

        Returns:
            Dictionary of configuration values.
        """
        try:
            raw_config = self.configpath.read_text()
        except FileNotFoundError:
            default_path = pathlib.Path(self.default_config)
            raw_config = default_path.read_text()
        return self._yaml.load(raw_config)

    def save(self) -> None:
        """Save the configuration."""
        if self._parent:
            self._parent.save()
        else:
            with self.configpath.open('w', encoding='utf-8') as file_:
                self.log.debug('configpath=%s file=%s', self.configpath, file_)
                self._yaml.dump(self._config, file_)

    def _as_config(self, dict_: Union[str, int, List, Dict]) -> Union[str, int, List, 'Config']:
        """Save config inside config.

        Args:
          dict_: Piece of configuration.

        Returns:
            Configuration as a dictionary.
        """
        if isinstance(dict_, collections.abc.MutableMapping):
            return Config(_parent=self, _config=dict_)
        return dict_

    def __getitem__(self, item: str) -> Value:
        if item not in self._config:
            raise KeyError(item)
        return self._config[item]

    def __setitem__(self, key: str, value: Value) -> None:
        self._config[key] = self._as_config(value)
        self.save()

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr: str, value: Value) -> None:
        if attr.startswith("_"):
            self.__dict__[attr] = value
        else:
            self.__setitem__(attr, value)

    def __delitem__(self, key: str) -> None:
        del self._config[key]

    def __iter__(self):
        for item in self._config:
            yield item

    def __len__(self) -> int:
        return len(self._config)

    def __repr__(self) -> str:
        return repr(self._config)

    def __str__(self) -> str:
        return str(self.__repr__())
