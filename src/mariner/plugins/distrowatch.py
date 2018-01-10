# -*- coding: future_fstrings -*-
"""Module for searching torrents on Distrowatch."""
import asyncio
import logging
from typing import List, Iterable, Tuple

import bs4

from mariner import searchengine, torrent, cache

Url = str
Page = str
Name = str


class Distrowatch(searchengine.SearchEngine):
    """Represent Distrowatch search engine."""

    log = logging.getLogger(__name__)
    search_url = "https://distrowatch.com/dwres.php?resource=bittorrent"

    async def get_results(self, title: str) -> None:
        """Get of list of torrent page urls.

        Args:
            title: String to search for.
        """
        try:
            page = await self.get(self.search_url)
        except OSError:
            print('Cannot reach server')
        else:
            self.urls = self._parse(page)

    @cache.Cache(size=100)
    def get_torrents(self, title: str) -> Iterable[torrent.Torrent]:
        """Get a list of torrents that we searched for.

        Args:
            title: String to search for.

        Returns:
            List of torrent results.
        """
        tid = 0
        torrents = []

        if not self.urls:
            self.log.debug('Fetching results')
            tasks = asyncio.wait([self.get_results(title)])
            loop = asyncio.get_event_loop()
            loop.run_until_complete(tasks)

        for name, url in self.urls:
            if title.lower() in name:
                self.log.debug('Appending tid=%s name=%s', tid, name)
                torrents.append(torrent.Torrent(tid, name, url))
                tid += 1
        return torrents

    @staticmethod
    def _parse(raw: str) -> List[Tuple[Name, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML page.

        Returns:
            List of torrent names with URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        torrents = soup.find_all('td', 'torrent')
        results = []
        for torrent_ in torrents:
            link = torrent_.find('a')
            name = link.string.lower()
            url_stub = link.get('href')
            url = f"https://distrowatch.com/{url_stub}"
            results.append((name, url))
        return results
