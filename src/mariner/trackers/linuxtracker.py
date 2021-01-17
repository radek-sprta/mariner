"""Module for searching torrents on LinuxTracker."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class LinuxTracker(trackerplugin.TrackerPlugin):
    """Represents LinuxTracker search engine."""

    log = logging.getLogger(__name__)

    filters = {"legal"}
    search_url = "https://linuxtracker.org/index.php?page=torrents&search={title}"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results page to parse.

        Returns:
            List of torrent names with magnet links.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        content = soup.find_all("table", {"class": "lista", "width": "100%"})
        for torrent_ in content[3].select("td.lista"):
            try:
                name = str(torrent_.font.a.string)
                tracker = self.__class__.__name__

                links = torrent_.find_all("td", {"align": "right"})[0]
                magnet = links.find_all("a")[0]["href"]
                stub = links.find_all("a")[1]["href"]
                url = f"http://linuxtracker.org/{stub}"

                details = torrent_.find_all("tr")
                date = details[0].get_text().strip().split()[2]
                size = " ".join(details[1].get_text().split()[1:])
                raw_seeds = details[2].get_text().split()[1]
                seeds = parse.number(raw_seeds)
                raw_leeches = details[3].get_text().split()[1]
                leeches = parse.number(raw_leeches)

                yield torrent.Torrent(
                    name,
                    tracker,
                    torrent=url,
                    magnet=magnet,
                    date=date,
                    size=size,
                    seeds=seeds,
                    leeches=leeches,
                )
            except AttributeError:
                pass
