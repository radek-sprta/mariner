"""Module for searching torrents on Etree."""
import asyncio
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin
from mariner.utils import parse


class Etree(trackerplugin.TrackerPlugin):
    """Represents Etree search engine."""

    log = logging.getLogger(__name__)

    filters = {"legal"}
    search_url = "https://bt.etree.org/?searchzzzz={title}"

    async def results(self, title: str) -> Iterator[torrent.Torrent]:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            search_url = self.search_url.format(title=title)
            page = await self.get(search_url, headers=self.user_agent, timeout=self.timeout)
        except (OSError, asyncio.TimeoutError):
            self.log.error("Cannot reach server at %s", search_url)
            return iter([])
        return (t for t in self._parse(page) if title in t.name.casefold())

    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:  # pylint: disable=too-many-locals
        """Parse result page.

        Args:
          raw: Raw HTML results to parse.

        Returns:
            List of torrent names with magnet links and URLs.
        """
        soup = bs4.BeautifulSoup(raw, "lxml")
        try:
            contents = soup.select("table")[5].select("tr")[1:]
            for content in contents:
                data = content.select("td")
                name = str(data[1].a.string)
                tracker = self.__class__.__name__

                url_stub = data[2].a.get("href")
                url = f"http://bt.etree.org/{url_stub}"

                size = str(data[6].string)
                date = str(data[5].string)
                seeds = parse.number(data[8].a.string)
                leeches = parse.number(data[9].a.string)

                yield torrent.Torrent(
                    name, tracker, torrent=url, size=size, date=date, seeds=seeds, leeches=leeches
                )
        except IndexError:
            yield from []
