# -*- coding: future_fstrings -*-
"""Module for searching torrents on KickAssTorrents."""
import asyncio
from typing import Dict, Iterator

import aiohttp
import bs4

from mariner import torrent, trackerplugin


class KickAssTorrents(trackerplugin.TrackerPlugin):
    """Represents KickAssTorrents search engine."""

    search_url = 'https://katcr.co/katsearch/page/1/{title}'
    aliases = ['kat']

    async def get_cookie(self, url: str) -> Dict:
        """Get KickAssTorrents session ID cookie.

        Args:
            url: Search page to get the cookie from.

        Returns:
            KickAssTorrents session cookie.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=self.timeout) as response:
                cookie = response.cookies.popitem()
                return {cookie[0]: cookie[1].value}

    async def results(self, title: str) -> Iterator[torrent.Torrent]:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            search_url = self.search_url.format(title=title)
            cookie = await self.get_cookie(search_url)
            page = await self.get(search_url, cookies=cookie)
        except (OSError, asyncio.TimeoutError):
            self.log.error('Cannot reach server at %s', search_url)
        return self._parse(page)

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results page to parse.

        Returns:
            List of torrent names with magnet links.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        contents = soup.find('table', class_='torrents_table')
        try:
            for line in contents.find_all('tr')[1:]:
                torrent_ = line.find(
                    'div', class_='torrents_table__torrent_name')
                name = str(torrent_.find(
                    'a', class_='torrents_table__torrent_title').b.string.strip())
                magnet = torrent_.find(
                    'a', {'title': 'Torrent magnet link'})['href']
                tracker = self.__class__.__name__
                size = line.find('td', {'data-title': 'Size'}).get_text().strip()
                date = line.find('td', {'data-title': 'Age'}).get_text()
                raw_seeds = line.find('td', {'data-title': 'Seed'}).string
                seeds = self._parse_number(raw_seeds)
                raw_leeches = line.find('td', {'data-title': 'Leech'}).string
                leeches = self._parse_number(raw_leeches)
                yield torrent.Torrent(name, tracker, magnet=magnet, size=size,
                                      date=date, seeds=seeds, leeches=leeches)
        except AttributeError:
            self.log.debug("No results found")
            yield from []
