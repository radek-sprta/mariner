"""Module for searching torrents on NyaaPantsu."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class NyaaPantsu(trackerplugin.TrackerPlugin):
    """Represents NyaaPantsu.com search engine."""

    log = logging.getLogger(__name__)

    filters = {"anime"}
    search_url = "https://nyaa.net/search?c=_&q={title}"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("tbody#torrentListResults tr")
            for content in contents:
                data = content.select("td")
                name = str(data[1].select("a")[0].string).strip()
                tracker = self.__class__.__name__

                links = data[2].select("a")
                magnet = links[0].get("href")
                url = links[1].get("href")

                size = str(data[3].string).strip()
                seeds = parse.number(data[4].text)
                leeches = parse.number(data[5].text)
                date = str(data[7].string)

                yield torrent.Torrent(
                    name,
                    tracker,
                    magnet=magnet,
                    torrent=url,
                    size=size,
                    seeds=seeds,
                    leeches=leeches,
                    date=date,
                )
        except IndexError:
            yield from []
