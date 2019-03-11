# -*- coding: future_fstrings -*-
"""Module for searching torrents on BTKitty."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin


class BTKitty(trackerplugin.TrackerPlugin):
    """Represents BTKitty search engine."""

    log = logging.getLogger(__name__)

    data = {"keyword": "{title}", "hidden": "true"}
    filters = {"dht"}
    request_method = "post"
    search_url = "http://btkitty.pet/"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("div.list-box dl.list-con")
            for content in contents:
                name = str(content.select("dt a")[0].text)
                tracker = self.__class__.__name__

                data = content.select("dd.option span")
                magnet = data[1].select("a")[0].get("href")
                date = str(data[2].select("b")[0].string)
                size = str(data[3].select("b")[0].string)
                seeds = int(int(data[6].select("b")[0].string) / 100)

                yield torrent.Torrent(
                    name,
                    tracker,
                    magnet=magnet,
                    torrent=None,
                    size=size,
                    date=date,
                    seeds=seeds,
                )
        except IndexError:
            yield from []
