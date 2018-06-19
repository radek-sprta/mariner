"""Base class for adding torrent tracker support."""
import abc
import asyncio
import logging
from typing import Iterator

from mariner import exceptions, mixins, torrent, proxyplugin

Url = str
Page = str


class TrackerMeta(abc.ABCMeta, type):
    """Metaclass to check that Tracker plugins override search_url."""
    def __new__(mcs, name, bases, namespace, **kwargs):
        if abc.ABC not in bases:
            if not namespace.get('search_url'):
                raise exceptions.PluginError('You must define search_url')
        return type.__new__(mcs, name, bases, namespace)


class TrackerPlugin(mixins.GetPageMixin, abc.ABC, metaclass=TrackerMeta):
    """Represent a search engine."""
    log = logging.getLogger(__name__)
    user_agent = {'user-agent': 'Mariner Torrent Downloader'}
    aliases = []  # Aliases for the tracker name
    legal = False

    search_url = ''  # To be overwritten by subclasses

    def __init__(self, timeout: int = 10) -> None:
        super().__init__()
        self.timeout = timeout

    async def results(self, title: str) -> Iterator:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            search_url = self.search_url.format(title=title)
            page = await self.get(search_url, timeout=self.timeout)
        except (OSError, asyncio.TimeoutError):
            self.log.error('Cannot reach server at %s', search_url)
            return iter([])
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


class ProxyTrackerPlugin(mixins.GetPageMixin, abc.ABC, metaclass=TrackerMeta):
    """Base class for trackers, that support alternative proxies.

    Attributes:
        proxies: Override with instance of ProxyPlugin.
    """
    log = logging.getLogger(__name__)
    user_agent = {'user-agent': 'Mariner Torrent Downloader'}
    aliases = []  # Aliases for the tracker name
    legal = False

    search_url = ''  # To be overwritten by subclasses
    default_proxy = ''  # To be overwritten by subclasses

    def __init__(self, timeout: int = 10) -> None:
        super().__init__()
        self.proxies = proxyplugin.ProxyPlugin()
        self.timeout = timeout

    async def get_proxy(self) -> str:
        """Return a responding proxy.

        Returns:
            URL for responding proxy.
        """
        return await self.proxies.get_proxy()

    async def results(self, title: str) -> Iterator:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            proxy = await self.get_proxy()
            search_url = self.search_url.format(proxy=proxy, title=title)
            page = await self.get(search_url)
        except (OSError, asyncio.TimeoutError):
            self.log.error('Cannot reach server at %s', search_url)
            return iter([])
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
