# -*- coding: future_fstrings -*-
"""Module for searching torrents on PirateBay."""
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.proxies import piratebay


class PirateBay(trackerplugin.ProxyTrackerPlugin):
    """Represents PirateBay search engine."""

    search_url = '{proxy}/search/{title}'
    aliases = ['tpb', 'pb']

    def __init__(self, timeout: int = 10) -> None:
        super().__init__()
        self.proxies = piratebay.PirateBayProxy()

    async def get_proxy(self) -> str:
        """Return a responding proxy.

        Returns:
            URL for responding proxy.
        """
        return await self.proxies.get_proxy()

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
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
            yield from []
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
    def _parse_name(raw: bs4.NavigableString) -> str:
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
