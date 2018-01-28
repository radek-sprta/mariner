# -*- coding: future_fstrings -*-
"""Module for searching torrents on Distrowatch."""
import asyncio
import logging
from typing import List, Tuple

import bs4

from mariner import searchengine, torrent

Url = str
Page = str
Name = str


class Distrowatch(searchengine.TrackerPlugin):
    """Represent Distrowatch search engine."""

    log = logging.getLogger(__name__)
    search_url = "https://distrowatch.com/dwres.php?resource=bittorrent"

    async def results(self, title: str) -> List[torrent.Torrent]:
        """Get of list of torrent page urls.

        Args:
            title: String to search for.
        """
        try:
            page = await self.get(self.search_url)
        except (OSError, asyncio.TimeoutError):
            print('Cannot reach server')
        else:
            return (t for t in self._parse(page) if title in t.name)

    def _parse(self, raw: str) -> List[Tuple[Name, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML page.

        Returns:
            List of torrent names with URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        content = soup.find('table', cellpadding='5').find_all('tr')[1:]
        for line in content:
            torrent_ = line.find('td', 'torrent')
            link = torrent_.find('a')
            name = link.string.lower()
            url_stub = link.get('href')
            url = f"https://distrowatch.com/{url_stub}"
            tracker = self.__class__.__name__
            date = str(line.find('td', 'torrentdate').string)
            yield torrent.Torrent(name, tracker, torrent=url, date=date)
