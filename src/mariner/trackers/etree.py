# -*- coding: future_fstrings -*-
"""Module for searching torrents on Etree."""
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin


class Etree(trackerplugin.TrackerPlugin):
    """Represents Etree search engine."""

    search_url = 'http://bt.etree.org/?searchzz={title}'

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        try:
            contents = soup.select('table')[5].select('tr')[1:]
            for content in contents:
                data = content.select('td')
                name = str(data[1].a.string)
                tracker = self.__class__.__name__

                url_stub = data[2].a.get('href')
                url = f'http://bt.etree.org/{url_stub}'

                size = str(data[6].string)
                date = str(data[5].string)
                seeds = self._parse_number(data[8].a.string)
                leeches = self._parse_number(data[9].a.string)

                yield torrent.Torrent(
                    name,
                    tracker,
                    torrent=url,
                    size=size,
                    date=date,
                    seeds=seeds,
                    leeches=leeches)
        except IndexError:
            yield from ()
