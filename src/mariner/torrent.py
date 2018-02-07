# -*- coding: future_fstrings -*-
"""Represent a downloadable torrent."""
import maya

from mariner import mixins


class Torrent(mixins.ComparableMixin):  # pylint: disable=too-many-instance-attributes
    """Class representing a Torrent."""

    def __init__(self,
                 name: str,
                 tracker: str,
                 *,
                 torrent: str = None,
                 magnet: str = None,
                 size: str = 'Unknown',
                 seeds: int = -1,
                 leeches: int = None,
                 date: str = None,
                 ) -> None:  # pylint: disable=bad-continuation
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
    def date(self) -> maya.core.MayaDT:
        """Upload date in structured format."""
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        try:
            self._date = maya.when(value)  # pylint: disable=attribute-defined-outside-init
        except ValueError:
            self._date = maya.parse(value)  # pylint: disable=attribute-defined-outside-init
        except TypeError:
            self._date = None  # pylint: disable=attribute-defined-outside-init

    @property
    def filename(self) -> str:
        """Filename to use for the torrent."""
        return self.name if '.torrent' in self.name else f'{self.name}.torrent'

    def __repr__(self) -> str:
        return f"Torrent({self.name}, {self.tracker}, {self.torrent}, \
    {self.magnet}, {self.size}, {self.seeds}, {self.leeches}, {self.date})"

    def __str__(self) -> str:
        return self.__repr__()
