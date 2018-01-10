"""Represent a downloadable torrent."""
from typing import Optional


class Torrent:
    """Class representing a Torrent."""

    def __init__(self,
                 tid: int,
                 name: str,
                 torrent_url: str,
                 *,
                 magnet_link: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        self.tid = tid
        self.name = name
        self.torrent_url = torrent_url
        self.magnet_link = magnet_link
        self.description = description

    @property
    def tid(self) -> int:
        """ID of the torrent."""
        return self.__tid

    @tid.setter
    def tid(self, value: int) -> None:
        if value < 0:
            raise ValueError("ID must be a positive number")
        else:
            self.__tid = value  # pylint: disable=attribute-defined-outside-init

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
        if '.torrent' in self.name:
            return self.name
        return f'{self.name}.torrent'

    def __repr__(self) -> str:
        return f"Torrent({self.tid}, {self.name}, {self.torrent_url}," \
            "{self.magnet_link}, {self.description})"

    def __str__(self) -> str:
        return self.__repr__()
