# -*- coding: future_fstrings -*-
"""Module for searching torrents on Distrowatch."""
import asyncio
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin


class Distrowatch(trackerplugin.TrackerPlugin):
    """Represent Distrowatch search engine."""

    log = logging.getLogger(__name__)
    search_url = "https://distrowatch.com/dwres.php?resource=bittorrent"
    legal = True

    async def results(self, title: str) -> Iterator[torrent.Torrent]:
        """Get of list of torrent page urls.

        Args:
            title: String to search for.
        """
        try:
            page = await self.get(self.search_url)
        except (OSError, asyncio.TimeoutError):
            print('Cannot reach server')
        return (t for t in self._parse(page) if title in t.name)

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:
        """Parse result page.

        Args:
          raw: Raw HTML page.

        Returns:
            List of torrent names with URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        content = soup.find('table', cellpadding='5').find_all('tr')[1:]
        for line in content:
            info = line.select('td.torrent')[1]
            name = str(info.a.string.lower())
            url_stub = info.a.get('href')
            url = f"https://distrowatch.com/{url_stub}"
            tracker = self.__class__.__name__
            date = str(line.select('td.torrentdate')[0].string)
            yield torrent.Torrent(name, tracker, torrent=url, date=date)
