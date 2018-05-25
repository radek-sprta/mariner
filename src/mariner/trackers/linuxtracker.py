# -*- coding: future_fstrings -*-
"""Module for searching torrents on LinuxTracker."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin


class LinuxTracker(trackerplugin.TrackerPlugin):
    """Represents LinuxTracker search engine."""

    log = logging.getLogger(__name__)

    search_url = 'http://linuxtracker.org/index.php?page=torrents&search={title}'
    legal = True

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results page to parse.

        Returns:
            List of torrent names with magnet links.
        """
        soup = bs4.BeautifulSoup(raw, 'lxml')
        content = soup.find_all('table', {'class': 'lista', 'width': '100%'})
        for torrent_ in content[4]:
            try:
                name = str(torrent_.font.a.string)
                tracker = self.__class__.__name__

                links = torrent_.find_all('td', {'align': 'right'})[0]
                magnet = links.find_all('a')[0]['href']
                stub = links.find_all('a')[1]['href']
                url = f'http://linuxtracker.org/{stub}'

                details = torrent_.find_all('tr')
                date = details[0].get_text().strip().split()[2]
                size = ' '.join(details[1].get_text().split()[1:])
                raw_seeds = details[2].get_text().split()[1]
                seeds = self._parse_number(raw_seeds)
                raw_leeches = details[3].get_text().split()[1]
                leeches = self._parse_number(raw_leeches)

                yield torrent.Torrent(name, tracker, torrent=url, magnet=magnet,
                                      date=date, size=size, seeds=seeds, leeches=leeches)
            except AttributeError:
                pass
