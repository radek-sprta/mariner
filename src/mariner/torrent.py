# -*- coding: future_fstrings -*-
"""Represent a downloadable torrent."""
import datetime
from typing import Union

from mariner import mixins, utils


class Torrent(mixins.ComparableMixin):  # pylint: disable=too-many-instance-attributes
    """Class representing a Torrent."""

    def __init__(self,
                 name: str,
                 tracker: str,
                 *,
                 torrent: str = None,
                 magnet: str = None,
                 size: str = 'Unknown',
                 seeds: Union[int, str] = -1,
                 leeches: Union[int, str] = None,
                 date: Union[datetime.date, str] = datetime.date(1, 1, 1)) -> None:
        self.name = name
        self.tracker = tracker
        self.torrent = torrent
        self.magnet = magnet
        self.size = size
        self.seeds = seeds
        self.leeches = leeches
        self.date = date

    @property
    def _cmpkey(self) -> int:
        """Key to use for torrent comparison."""
        return self.seeds

    @property
    def date(self) -> datetime.date:
        """Upload date in structured format."""
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        if isinstance(value, (datetime.date, type(None))):
            self._date = value  # pylint: disable=attribute-defined-outside-init
        else:
            # Defer importing maya, as it is a slow import
            import maya
            try:
                self._date = maya.when(value).date  # pylint: disable=attribute-defined-outside-init
            except ValueError:
                self._date = maya.parse(value).date  # pylint: disable=W0201
            except TypeError:
                self._date = datetime.date(1, 1, 1)  # pylint: disable=W0201

    @property
    def filename(self) -> str:
        """Filename to use for the torrent."""
        return self.name if '.torrent' in self.name else f'{self.name}.torrent'

    def colored(self) -> 'Torrent':
        """Return Torrent with colored fields."""
        return Torrent(name=utils.yellow(self.name[:80]),
                       tracker=self.tracker,
                       torrent=self.torrent,
                       magnet=self.magnet,
                       size=self.size,
                       seeds=utils.green(self.seeds),
                       leeches=utils.red(
                           self.leeches) if self.leeches is not None else None,
                       date=self.date)

    def __repr__(self) -> str:
        return f"Torrent({self.name}, {self.tracker}, {self.torrent}, \
{self.magnet}, {self.size}, {self.seeds}, {self.leeches}, {self.date})"

    def __str__(self) -> str:
        return self.__repr__()
