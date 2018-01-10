"""Module for searching torrents on TokyoTosho."""
from typing import List, Tuple

import bs4

from mariner import searchengine

Magnet = str
Name = str
Url = str


class TokyoTosho(searchengine.SearchEngine):
    """Represents TokyoTosho search engine."""

    search_url = 'https://www.tokyotosho.info/search.php?terms='

    @staticmethod
    def _parse(raw: str) -> List[Tuple[Name, Magnet, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        torrents = soup.select('.desc-top')
        results = []
        for torrent_ in torrents:
            links = torrent_.select('a')
            magnet = links[0].get('href')
            url = links[1].get('href')
            name = TokyoTosho._parse_name(links[1].contents)
            results.append((name, magnet, url))
        return results

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
