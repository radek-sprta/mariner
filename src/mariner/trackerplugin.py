"""Base class for adding torrent tracker support."""
import abc
import asyncio
import logging
from typing import Iterator

import aiohttp
import async_timeout

from mariner import exceptions, torrent

Url = str
Page = str


class TrackerMeta(abc.ABCMeta, type):
    """Metaclass to check, that Tracket plugins override search_url."""
    def __new__(mcs, name, bases, namespace, **kwargs):
        if bases != (abc.ABC,):
            if not namespace.get('search_url'):
                raise exceptions.InputError('You must define search_url')
        return type.__new__(mcs, name, bases, namespace)


class TrackerPlugin(abc.ABC, metaclass=TrackerMeta):
    """Represent a search engine."""
    log = logging.getLogger(__name__)
    user_agent = {'user-agent': 'Mariner Torrent Downloader'}
    search_url = ''  # To be overwritten by subclasses
    aliases = []  # Aliases for the tracker name

    async def get(self, url: Url) -> Page:
        """Asynchronous https request.

        Args:
            url: Url of the webpage to fetch.

        Returns:
            Fetched webpage."""
        self.log.debug('Fetching url=%s', url)
        with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.user_agent) as response:
                    page = await response.text()
        return page

    async def results(self, title: str) -> Iterator[torrent.Torrent]:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            search_url = self.search_url + title
            page = await self.get(search_url)
        except (OSError, asyncio.TimeoutError):
            self.log.error('Cannot reach server at %s', search_url)
        return self._parse(page)

    @abc.abstractmethod
    def _parse(self, raw: str) -> Iterator[torrent.Torrent]:
        """Parse result page.

        Args:
            raw: Raw HTML page.

        Returns:
            List of torrents names with URLs and magnet links.

        """
        raise NotImplementedError

    @staticmethod
    def _parse_number(number: str) -> int:
        """Parse a number string from HTML page and return an interger.

        Args:
            number: Number string to parse.

        Return:
            Parsed number.
        """
        squashed = number.replace(' ', '')
        return int(squashed.replace(',', ''))
