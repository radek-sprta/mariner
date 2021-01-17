"""Module for searching torrents on TokyoTosho."""
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class TokyoTosho(trackerplugin.TrackerPlugin):
    """Represents TokyoTosho search engine."""

    log = logging.getLogger(__name__)

    aliases = ["tt"]
    filters = {"anime"}
    search_url = "https://www.tokyotosho.info/search.php?terms={title}"

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        contents = soup.select("tr.category_0")
        for content in contents:
            try:
                # Even lines
                torrent_ = content.select(".desc-top")[0]
                links = torrent_.select("a")
                magnet = links[0].get("href")
                url = links[1].get("href")
                name = TokyoTosho._parse_name(links[1].contents)
                tracker = self.__class__.__name__
                result = torrent.Torrent(name, tracker, magnet=magnet, torrent=url)
            except IndexError:
                # Odd lines
                details = content.select("td.desc-bot")[0].get_text().split("|")
                result.size = details[1].split(":")[1].strip()
                result.date = details[2].split()[1]

                stats = content.select("td.stats")[0].select("span")
                raw_seeds = stats[0].string
                result.seeds = parse.number(raw_seeds)
                raw_leeches = stats[1].string
                result.leeches = parse.number(raw_leeches)
                yield result

    @staticmethod
    def _parse_name(raw: bs4.NavigableString) -> str:
        """Parse torrent name.

        Args:
          raw: Raw HTML name to parse.

        Returns:
            Parsed name.
        """
        name = [c for c in raw if isinstance(c, bs4.element.NavigableString)]
        return "".join(name)
