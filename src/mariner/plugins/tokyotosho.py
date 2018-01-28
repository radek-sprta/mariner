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

    def _parse(self, raw: str) -> List[Tuple[Name, Magnet, Url]]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        contents = soup.select('tr.category_0')
        for content in contents:
            try:
                # Even lines
                torrent_ = content.select('.desc-top')[0]
                links = torrent_.select('a')
                magnet = links[0].get('href')
                url = links[1].get('href')
                name = TokyoTosho._parse_name(links[1].contents)
                tracker = self.__class__.__name__
                result = torrent.Torrent(
                    name, tracker, magnet=magnet, torrent=url)
            except IndexError:
                # Odd lines
                details = content.select(
                    'td.desc-bot')[0].get_text().split('|')
                result.size = details[1].split(':')[1].strip()
                result.date = details[2].split()[1]

                stats = content.select('td.stats')[0].select('span')
                raw_seeds = stats[0].string
                result.seeds = self._parse_number(raw_seeds)
                raw_leeches = stats[1].string
                result.leeches = self._parse_number(raw_leeches)
                yield result

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
