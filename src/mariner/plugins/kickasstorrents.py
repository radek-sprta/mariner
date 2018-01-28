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
    aliases = ['kat']

    def _parse(self, raw: str) -> List[Tuple[Name, Magnet, Url]]:  # pylint: disable=too-many-locals
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
                    'a', class_='torrents_table__torrent_title').string)
                magnet = torrent_.find(
                    'a', {'title': 'Torrent magnet link'})['href']
                tracker = self.__class__.__name__
                size = line.find('td', {'data-title': 'Size'}).get_text()
                date = line.find('td', {'data-title': 'Age'}).get_text()
                raw_seeds = line.find('td', {'data-title': 'Seed'}).string
                seeds = self._parse_number(raw_seeds)
                raw_leeches = line.find('td', {'data-title': 'Leech'}).string
                leeches = self._parse_number(raw_leeches)
                yield torrent.Torrent(name, tracker, magnet=magnet, size=size,
                                      date=date, seeds=seeds, leeches=leeches)
        except AttributeError:
            self.log.debug("No results found")
            yield from ()
