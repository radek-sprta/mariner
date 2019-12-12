# -*- coding: future_fstrings -*-
"""Module for searching torrents on Anidex."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class Anidex(trackerplugin.TrackerPlugin):
    """Represents Anidex.info search engine."""

    log = logging.getLogger(__name__)

    filters = {"anime"}
    search_url = "https://anidex.info/?q={title}&s=seeders&o=desc"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("table.table-striped tbody tr")
            for content in contents:
                data = content.select("td")
                name = str(data[2].select("span.span-1440")[0].string)
                tracker = self.__class__.__name__

                url_stub = data[4].select("a")[0].get("href")
                url = f"https://anidex.info{url_stub}"
                magnet = data[5].select("a")[0].get("href")

                size = str(data[6].string)
                date = str(data[7].string)
                seeds = parse.number(data[8].text)
                leeches = parse.number(data[9].string)

                yield torrent.Torrent(
                    name,
                    tracker,
                    magnet=magnet,
                    torrent=url,
                    size=size,
                    date=date,
                    seeds=seeds,
                    leeches=leeches,
                )
        except IndexError:
            yield from []
