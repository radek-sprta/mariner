"""Module for searching torrents on KickAssTorrents."""
from typing import List, Tuple

import bs4

from mariner import searchengine, torrent

Magnet = str
Name = str
Url = str


class KickAssTorrents(searchengine.TrackerPlugin):
    """Represents KickAssTorrents search engine."""

    search_url = 'https://katcr.co/katsearch/page/1/'

    def _parse(self, raw: str) -> List[Tuple[Name, Magnet, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML results page to parse.

        Returns:
            List of torrent names with magnet links.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        content = soup.find_all('div', class_='torrents_table__torrent_name')
        results = []
        try:
            for torrent_ in content:
                name = str(torrent_.find(
                    'a', class_='torrents_table__torrent_title').string)
                magnet = torrent_.find(
                    'a', {'title': 'Torrent magnet link'})['href']
                tracker = self.__class__.__name__
                results.append(torrent.Torrent(
                    name, tracker, magnet_link=magnet))
        except AttributeError:
            self.log.debug("No results found")
        return results
