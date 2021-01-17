"""Module for searching torrents on Nyaa."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class Nyaa(trackerplugin.TrackerPlugin):
    """Represents Nyaa.si search engine."""

    log = logging.getLogger(__name__)

    filters = {"anime"}
    search_url = "https://nyaa.si/?f=0&c=0_0&q={title}"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("tr.default")
            for content in contents:
                data = content.select("td")
                # Sometimes title is preceded by comments, so choose the last <a>
                name = str(data[1].select("a")[-1].string)
                tracker = self.__class__.__name__

                links = data[2].select("a")
                url_stub = links[0].get("href")
                url = f"https://nyaa.si{url_stub}"
                magnet = links[1].get("href")

                size = str(data[3].string)
                date = str(data[4].string)
                seeds = parse.number(data[5].string)
                leeches = parse.number(data[6].string)

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
