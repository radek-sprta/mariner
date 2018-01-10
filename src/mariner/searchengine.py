# -*- coding: future_fstrings -*-
"""Handle searching for torrents on torrent trackers."""
import abc
import asyncio
import importlib
import logging
import pathlib
from typing import List, Iterable, Tuple, Optional, Union

import aiohttp
import async_timeout

from mariner import torrent, cache

Name = str
Page = str
Path = Union[str, pathlib.Path]
Url = str

engines = {}


class SearchEngineManager:
    """Manage search engine plugins."""
    log = logging.getLogger(__name__)

    def __init__(self, path: Path = None) -> None:
        if not path:
            self.engine_directory = pathlib.Path(__file__).parent / 'plugins'
        else:
            self.engine_directory = pathlib.Path(path)
        self.log.debug('path=%s engine_directory=%s',
                       path, self.engine_directory)

    def find_engines(self) -> None:
        """Find and import search engines."""
        for module in self.engine_directory.glob('*.py'):
            self.log.debug('Loading module=%s', module)
            if module.name != '__init__.py':
                name = module.stem
                spec = importlib.util.spec_from_file_location(name, module)
                loaded_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(loaded_module)

    def register_engines(self) -> None:
        """Register search engines into global namespace."""
        for engine in SearchEngine.__subclasses__():
            self.log.debug('Adding engine=%s', engine)
            name = engine.__name__.lower()
            engines[name] = engine

    def initialize_engines(self) -> None:
        """Find engines and put them into global namespace."""
        self.log.info('Initializing plugins')
        self.find_engines()
        self.register_engines()


class SearchEngine(abc.ABC):
    """Represent a search engine."""
    log = logging.getLogger(__name__)
    user_agent = {'user-agent': 'Mariner Torrent Downloader'}
    search_url = ''  # To be overwritten by subclasses

    def __init__(self) -> None:
        super().__init__()
        self.results = []
        self.urls = []

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

    async def get_results(self, title: str) -> None:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            search_url = self.search_url + title
            page = await self.get(search_url)
        except (OSError, asyncio.TimeoutError):
            self.log.error('Cannot reach server')
        else:
            self.urls = self._parse(page)

    def get_torrent(self, tid: int) -> torrent.Torrent:
        """Get torrent of given id.

        Args:
            tid: ID of the torrents to get.

        Returns:
            Torrent with given ID.

        """
        if not self.results:
            self.log.debug('Fetching results from cache')
            self.results = list(cache.Cache().newest)
        if tid < 0 or tid > len(self.results):
            self.log.debug('tid=%s', tid)
            raise NoResultException(f"No torrent with ID {tid}")
        return self.results[tid]

    @cache.Cache(size=100)
    def get_torrents(self, title: str) -> Iterable[torrent.Torrent]:
        """Get a list of torrents that we searched for.

        Args:
           title: String to search for.

        Returns:
            List of torrent results.
        """
        if not self.urls:
            self.log.debug('Fetching search results')
            tasks = asyncio.wait([self.get_results(title)])
            loop = asyncio.get_event_loop()
            loop.run_until_complete(tasks)

        tid = 0
        torrents = []
        for name, magnet, url in self.urls:
            self.log.debug('Added tid=%s name=%s', tid, name)
            torrents.append(torrent.Torrent(
                tid, name, url, magnet_link=magnet))
            tid += 1
        return torrents

    @staticmethod
    @abc.abstractmethod
    def _parse(raw: str) -> List[Tuple[Name, Url]]:
        """Parse result page.

        Args:
            raw: Raw HTML page.

        Returns:
            List of torrents names with URLs and magnet links.

        """
        raise NotImplementedError

    def search(self, title: str, limit: Optional[int] = 10) -> List[torrent.Torrent]:
        """Search for torrents on given site.

        Args:
            title: String to search for.
            limit: Defaults to 10. Limits the number of results, that should be shown.

        Returns:
            List of Torrents returned by the search, up to the limit.
        """
        if not title:
            raise ValueError('No string to search for.')
        if limit <= 0:
            raise ValueError('Limit has to be higher than zero.')
        torrents = self.get_torrents(title)
        self.results = torrents[:limit]
        self.log.debug('Search results=%s', self.results)
        if self.results:
            return self.results
        raise NoResultException(f"No results for {title}")


class Error(Exception):
    """Base-class for all exceptions raised by this module."""


class NoResultException(Error):
    """No result found for given search string."""
