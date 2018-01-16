"""Module for searching torrents on TokyoTosho."""
from typing import List, Tuple

import bs4

from mariner import searchengine, torrent

Magnet = str
Name = str
Url = str


class TokyoTosho(searchengine.TrackerPlugin):
    """Represents TokyoTosho search engine."""

    search_url = 'https://www.tokyotosho.info/search.php?terms='

    def _parse(self, raw: str) -> List[Tuple[Name, Magnet, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        torrents = soup.select('.desc-top')
        for torrent_ in torrents:
            links = torrent_.select('a')
            magnet = links[0].get('href')
            url = links[1].get('href')
            name = TokyoTosho._parse_name(links[1].contents)
            tracker = self.__class__.__name__
            yield torrent.Torrent(name, tracker, magnet_link=magnet, torrent_url=url)

    @staticmethod
    def _parse_name(raw: str) -> Name:
        """Parse torrent name.

        Args:
          raw: Raw HTML name to parse.

        Returns:
            Parsed name.
        """
        name = [c for c in raw if isinstance(c, bs4.element.NavigableString)]
        return ''.join(name)
