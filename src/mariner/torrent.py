# -*- coding: future_fstrings -*-
"""Represent a downloadable torrent."""


class Torrent:
    """Class representing a Torrent."""

    def __init__(self,
                 name: str,
                 tracker: str,
                 *,
                 torrent_url: str = None,
                 magnet_link: str = None,
                 ) -> None:
        self.name = name
        self.torrent_url = torrent_url
        self.magnet_link = magnet_link
        self.tracker = tracker

    @property
    def mods(self) -> str:
        """Show whether it is available as torrent, magnet link or both."""
        mods = []
        if self.torrent_url:
            mods.append('Torrent')
        if self.magnet_link:
            mods.append('Magnet link')
        return ', '.join(mods)

    @property
    def filename(self) -> str:
        """Filename to use for the torrent."""
        return self.name if '.torrent' in self.name else f'{self.name}.torrent'

    def __repr__(self) -> str:
        return f"Torrent({self.name}, {self.tracker}, {self.torrent_url}, {self.magnet_link})"

    def __str__(self) -> str:
        return self.__repr__()
