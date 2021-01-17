"""Module for searching torrents on LimeTorrents."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class LimeTorrents(trackerplugin.TrackerPlugin):
    """Represents LimeTorrents search engine."""

    log = logging.getLogger(__name__)

    aliases = ["lime"]
    search_url = "https://limetorrents.info/search/all/{title}/seeds/1"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("table.table2")[0].select("tr")[1:]
            for content in contents:
                data = content.select("td")
                name = str(data[0].select("a")[1].string)
                tracker = self.__class__.__name__

                url = data[0].div.a.get("href")

                size = str(data[2].string)
                date = str(data[1].string.split("-")[0].strip())
                seeds = parse.number(data[3].string)
                leeches = parse.number(data[4].string)

                yield torrent.Torrent(
                    name, tracker, torrent=url, size=size, date=date, seeds=seeds, leeches=leeches
                )
        except IndexError:
            yield from []
