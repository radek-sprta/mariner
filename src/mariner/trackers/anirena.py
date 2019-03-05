# -*- coding: future_fstrings -*-
"""Module for searching torrents on Anirena."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin


class Anirena(trackerplugin.TrackerPlugin):
    """Represents Anirena.com search engine."""

    log = logging.getLogger(__name__)

    filters = {"anime"}
    search_url = "https://www.anirena.com/?s={title}"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("div.full2 table")
            for content in contents:
                data = content.select("tr td")
                name = str(data[1].select("a")[-1].string).strip()
                tracker = self.__class__.__name__

                links = data[2].select("a")
                url_stub = links[0].get("href")
                url = f"https://www.anirena.com{url_stub}"
                magnet = links[1].get("href")

                size = str(data[3].string)
                seeds = int(data[4].text)
                leeches = int(data[5].text)

                yield torrent.Torrent(
                    name,
                    tracker,
                    magnet=magnet,
                    torrent=url,
                    size=size,
                    seeds=seeds,
                    leeches=leeches,
                )
        except IndexError:
            yield from []
