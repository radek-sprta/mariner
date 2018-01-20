# -*- coding: future_fstrings -*-
"""Represent a downloadable torrent."""
from mariner import mixins


class Torrent(mixins.ComparableMixin):
    """Class representing a Torrent."""

    def __init__(self,
                 name: str,
                 tracker: str,
                 *,
                 torrent_url: str = None,
                 magnet_link: str = None,
                 seeds: int = -1,
                 ) -> None:  # pylint: disable=bad-continuation
        self.name = name
        self.tracker = tracker
        self.torrent_url = torrent_url
        self.magnet_link = magnet_link
        self.seeds = seeds

    @property
    def _cmpkey(self) -> int:
        """Key to use for torrent comparison."""
        return self.seeds

    @property
    def filename(self) -> str:
        """Filename to use for the torrent."""
        return self.name if '.torrent' in self.name else f'{self.name}.torrent'

    def __repr__(self) -> str:
        return f"Torrent({self.name}, {self.tracker}, {self.torrent_url}, {self.magnet_link}, {self.seeds})"

    def __str__(self) -> str:
        return self.__repr__()
