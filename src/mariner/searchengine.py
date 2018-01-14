# -*- coding: future_fstrings -*-
"""Handle searching for torrents on torrent trackers."""
import abc
import asyncio
import importlib
import itertools
import logging
import pathlib
from typing import List, Optional, Tuple, Union

import aiohttp
import async_timeout

from mariner import torrent, cache

Name = str
Page = str
Path = Union[str, pathlib.Path]
Url = str


class SearchEngine:
    """Search on for a torrent using Tracker plugins."""

    log = logging.getLogger(__name__)
    plugin_directory = pathlib.Path(__file__).parent / 'plugins'

    def __init__(self) -> None:
        self.plugins = {}
        self.results = cache.Cache(
            path='~/.local/share/mariner/results.json', size=1000)
        self.initialize_plugins()

    def _flatten(self, nested_list: List[List]) -> List:
        """Flatten a list."""
        return list(itertools.chain(*nested_list))

    def find_plugins(self) -> None:
        """Find and import tracker plugins."""
        for module in self.plugin_directory.glob('*.py'):
            self.log.debug('Loading module=%s', module)
            name = module.stem
            spec = importlib.util.spec_from_file_location(name, module)
            loaded_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded_module)

    def initialize_plugins(self) -> None:
        """Find engines and register them."""
        self.log.debug('Initializing plugins')
        self.find_plugins()
        for plugin in TrackerPlugin.__subclasses__():
            self.log.debug('Adding plugin=%s', plugin)
            name = plugin.__name__.lower()
            self.plugins[name] = plugin

    def result(self, tid: str) -> torrent.Torrent:
        """Get torrent of given id.

        Args:
            tid: ID of the torrent to get.

        Returns:
            Torrent with given ID.
        """
        self.log.debug('Fetching torrent with tid=%s', tid)
        torrent = self.results.get(tid)
        if torrent:
            return torrent
        raise NoResultException(f"No torrent with ID {tid}")

    @cache.Cache(size=100)
    def _cached_search(self,
                       title: str,
                       trackers: List[str],
                       ) -> List[torrent.Torrent]:
        """Search for torrents on given site and cache to results. This
        method is an implementation detail. As coroutines are not easily
        serializable, we cannot simply cache TrackerPlugun.results() method.

        Args:
            title: String to search for.

        Returns:
            List of Torrents returned by the search.
        """
        self.log.debug('Fetching search results')
        tasks = asyncio.gather(
            *[self.plugins[t]().results(title.lower()) for t in trackers])
        loop = asyncio.get_event_loop()
        torrents = loop.run_until_complete(tasks)
        torrents = self._flatten(torrents)
        return torrents

    def search(self,
               title: str,
               trackers: List[str],
               limit: Optional[int] = 10
               ) -> List[torrent.Torrent]:
        """Search for torrents on given site.

        Args:
            title: String to search for.
            limit: Defaults to 10. Limits the number of results, that should be shown.

        Returns:
            List of Torrents returned by the search, up to the limit.
        """
        if not title:
            raise ValueError('No string to search for.')
        if not trackers:
            raise ValueError('No torrent trackers to search on')
        if limit <= 0:
            raise ValueError('Limit has to be higher than zero.')

        torrents = self._cached_search(title, trackers)

        results = [(i, t) for i, t in enumerate(torrents[:limit])]
        if results:
            self.save_results(results)
            return results
        raise NoResultException(f"No results for {title}")

    def save_results(self, torrents: List[Tuple[int, torrent.Torrent]]) -> None:
        """Save results in a database.

        Args:
            torrents: List of ID, Torrent tuples.
        """
        self.results.clear()
        for tid, torrent_ in torrents:
            self.results.insert(tid, torrent_)


class TrackerMeta(abc.ABCMeta, type):
    """Metaclass to check, that Tracket plugins override search_url."""
    def __new__(meta, name, bases, class_dict):
        if bases != (abc.ABC,):
            if not class_dict.get('search_url'):
                raise ValueError('You must define search_url')
        return type.__new__(meta, name, bases, class_dict)


class TrackerPlugin(abc.ABC, metaclass=TrackerMeta):
    """Represent a search engine."""
    log = logging.getLogger(__name__)
    user_agent = {'user-agent': 'Mariner Torrent Downloader'}
    search_url = ''  # To be overwritten by subclasses

    def __init__(self) -> None:
        super().__init__()

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

    async def results(self, title: str) -> List[torrent.Torrent]:
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
            return self._parse(page)

    @abc.abstractmethod
    def _parse(self, raw: str) -> List[Tuple[Name, Url]]:
        """Parse result page.

        Args:
            raw: Raw HTML page.

        Returns:
            List of torrents names with URLs and magnet links.

        """
        raise NotImplementedError


class Error(Exception):
    """Base-class for all exceptions raised by this module."""


class NoResultException(Error):
    """No result found for given search string."""
