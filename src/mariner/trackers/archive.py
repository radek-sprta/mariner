"""Module for searching torrents on Archive."""
import asyncio
import logging
from typing import Iterator

import bs4

from mariner import torrent, trackerplugin


class Archive(trackerplugin.TrackerPlugin):
    """Represents Archive search engine."""

    log = logging.getLogger(__name__)

    filters = {"legal"}
    search_url = "https://archive.org/details/feature_films?and[]={title}&sin="

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
            contents = soup.select("div.results")[0].select("div.item-ia")[1:]
            for content in contents:
                name = str(content.select("div.ttl")[0].string.strip())
                tracker = self.__class__.__name__

                url_stub = content.get("data-id")
                url = f"https://archive.org/download/{url_stub}/{url_stub}_archive.torrent"

                yield torrent.Torrent(name, tracker, torrent=url)
        except IndexError:
            yield from []
