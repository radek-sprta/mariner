"""Module for searching torrents on PirateBay."""
from typing import List, Tuple

import bs4

from mariner import searchengine

Magnet = str
Name = str
Url = str


class PirateBay(searchengine.SearchEngine):
    """Represents PirateBay search engine."""

    search_url = 'https://thepiratebay.org/search/'

    @staticmethod
    def _parse(raw: str) -> List[Tuple[Name, Magnet, Url]]:
        """Parse result page.

        Args:
          raw: Raw HTML results page to parse.

        Returns:
            List of torrent names with magnet links.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        content = soup.find('table', id='searchResult')
        try:
            torrents = content.find_all('tr')
        except AttributeError:
            # No search result
            return []
        else:
            results = []
            for torrent_ in torrents[1:]:
                raw_name = torrent_.find('a', class_='detLink')
                name = PirateBay._parse_name(raw_name)

                links = torrent_.find_all('a')
                magnet = links[3].get('href')
                # PirateBay has only magnet links
                url = None

                results.append((name, magnet, url))
            return results

    @staticmethod
    def _parse_name(raw: str) -> Name:
        """Parse torrent name.

        Args:
          raw: Raw name to parse.

        Returns:
            Parsed name.
        """
        name = raw.string
        if name is None:
            name = raw['title'].split(" ")[2:]
            name = ' '.join(str(x) for x in name)
        return name.strip()
