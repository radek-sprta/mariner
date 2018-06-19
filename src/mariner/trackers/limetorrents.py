# -*- coding: future_fstrings -*-
"""Module for searching torrents on LimeTorrents."""
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.proxies import limetorrents


class LimeTorrents(trackerplugin.ProxyTrackerPlugin):
    """Represents LimeTorrents search engine."""

    search_url = '{proxy}/search/all/{title}/seeds/1'

    def __init__(self, timeout: int = 10) -> None:
        super().__init__()
        self.proxies = limetorrents.LimeTorrentsProxy()

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        try:
            contents = soup.select('table.table2')[0].select('tr')[1:]
            for content in contents:
                data = content.select('td')
                name = str(data[0].select('a')[1].string)
                tracker = self.__class__.__name__

                url = data[0].div.a.get('href')

                size = str(data[2].string)
                date = str(data[1].string.split('-')[0].strip())
                seeds = self._parse_number(data[3].string)
                leeches = self._parse_number(data[4].string)

                yield torrent.Torrent(
                    name,
                    tracker,
                    torrent=url,
                    size=size,
                    date=date,
                    seeds=seeds,
                    leeches=leeches)
        except IndexError:
            yield from []
