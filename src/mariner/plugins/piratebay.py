"""Module for searching torrents on PirateBay."""
from typing import List, Tuple

import bs4

from mariner import searchengine, torrent

Magnet = str
Name = str
Url = str


class PirateBay(searchengine.TrackerPlugin):
    """Represents PirateBay search engine."""

    search_url = 'https://thepiratebay.org/search/'
    aliases = ['tpb', 'pb']

    def _parse(self, raw: str) -> List[Tuple[Name, Magnet, Url]]:  # pylint: disable=too-many-locals
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
            yield from ()
        else:
            for torrent_ in torrents[1:]:
                raw_name = torrent_.find('a', class_='detLink')
                name = PirateBay._parse_name(raw_name)
                links = torrent_.find_all('a')
                magnet = links[3].get('href')
                tracker = self.__class__.__name__

                numbers = torrent_.find_all('td', align='right')
                raw_seeds = numbers[0].string
                seeds = self._parse_number(raw_seeds)
                raw_leeches = numbers[1].string
                leeches = self._parse_number(raw_leeches)

                description = torrent_.find(
                    'font', class_="detDesc").get_text()
                fields = description.split(',')
                date = ' '.join(fields[0].split()[1:])
                size = ' '.join(fields[1].split()[-2:])

                yield torrent.Torrent(name, tracker, magnet=magnet, seeds=seeds,
                                      leeches=leeches, date=date, size=size)

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
