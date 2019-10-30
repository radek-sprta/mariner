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

    def __new__(cls, name, bases, namespace, **kwargs):
        if abc.ABC not in bases:
            if not namespace.get("search_url"):
                raise exceptions.PluginError("You must define search_url")
        return type.__new__(cls, name, bases, namespace)


class TrackerPlugin(mixins.RequestMixin, abc.ABC, metaclass=TrackerMeta):
    """Represent a search engine."""

    log = logging.getLogger(__name__)
    aliases = []  # Aliases for the tracker name
    filters = set()

    data = {}
    request_method = "get"
    search_url = ""  # To be overwritten by subclasses

    def __init__(self, timeout: int = 10) -> None:
        super().__init__()
        self.timeout = timeout

    async def results(self, title: str) -> Iterator:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            if self.data:
                self.data["keyword"] = self.data.get("keyword").format(title=title)
            search_url = self.search_url.format(title=title)
            page = await self.request(
                self.request_method, search_url, data=self.data, timeout=self.timeout
            )
        except (OSError, asyncio.TimeoutError) as e:
            print(e)
            self.log.error("Cannot reach server at %s", search_url)
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


class ProxyTrackerPlugin(mixins.RequestMixin, abc.ABC, metaclass=TrackerMeta):
    """Base class for trackers, that support alternative proxies.

    Attributes:
        proxies: Override with instance of ProxyPlugin.
    """

    log = logging.getLogger(__name__)
    aliases = []  # Aliases for the tracker name
    filters = set()
    request_method = "get"

    search_url = ""  # To be overwritten by subclasses

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
        proxy = await self.get_proxy()
        search_url = self.search_url.format(proxy=proxy, title=title)
        try:
            page = await self.request(self.request_method, search_url, timeout=self.timeout)
        except (OSError, asyncio.TimeoutError) as e:
            print(e)
            self.log.error("Cannot reach server at %s", search_url)
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
