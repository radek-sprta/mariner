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
import cachalot

from mariner import torrent, exceptions

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
        self.results = cachalot.Cache(
            path='~/.local/share/mariner/results.json', size=1000)
        self.initialize_plugins()

    @staticmethod
    def _flatten(nested_list: List[List]) -> List:
        """Flatten a list."""
        return list(itertools.chain(*nested_list))

    def find_plugins(self) -> None:
        """Find and import tracker plugins."""
        for module in self.plugin_directory.glob('*.py'):  # pylint: disable=no-member
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
            for alias in plugin.aliases:
                self.plugins[alias] = plugin

    def result(self, tid: str) -> torrent.Torrent:
        """Get torrent of given id.

        Args:
            tid: ID of the torrent to get.

        Returns:
            Torrent with given ID.
        """
        self.log.debug('Fetching torrent with tid=%s', tid)
        torrent_ = self.results.get(tid)
        if torrent_:
            return torrent_
        raise exceptions.NoResultException(f"No torrent with ID {tid}")

    @cachalot.Cache(path='.cache/mariner/cache.json', size=100)
    def _cached_search(self,
                       title: str,
                       trackers: List[str],
                       ) -> List[torrent.Torrent]:  # pylint: disable=bad-continuation
        """Search for torrents on given site and cache to results. This
        method is an implementation detail. As coroutines are not easily
        serializable, we cannot simply cache TrackerPlugun.results() method.

        Args:
            title: String to search for.

        Returns:
            List of Torrents returned by the search.
        """
        self.log.debug('Fetching search results')

        # Get unique trackers
        try:
            plugins = set(self.plugins[t] for t in trackers)
        except KeyError:
            raise exceptions.ConfigurationError("Illegal value for default_tracker")
        else:
            tasks = asyncio.gather(*(p().results(title.lower()) for p in plugins))
            loop = asyncio.get_event_loop()
            torrents = loop.run_until_complete(tasks)
            torrents = self._flatten(torrents)
        return torrents

    def search(self,
               title: str,
               trackers: List[str],
               limit: Optional[int] = 10
               ) -> List[torrent.Torrent]:  # pylint: disable=bad-continuation
        """Search for torrents on given site.

        Args:
            title: String to search for.
            limit: Defaults to 10. Limits the number of results, that should be shown.

        Returns:
            List of Torrents returned by the search, up to the limit.
        """
        if not title:
            raise exceptions.InputError('No string to search for.')
        if not trackers:
            raise exceptions.InputError('No torrent trackers to search on')
        if limit <= 0:
            raise exceptions.InputError('Limit has to be higher than zero.')

        torrents = self._cached_search(title, trackers)
        sorted_torrents = list(reversed(sorted(torrents)))
        results = [(i, t) for i, t in enumerate(sorted_torrents[:limit])]
        if results:
            self.save_results(results)
            return results
        raise exceptions.NoResultException(f"No results for {title}")

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

    async def results(self, title: str) -> List[torrent.Torrent]:
        """Get a list of torrent name with URLs and magnet links.

        Args:
            title: String to search for.
        """
        try:
            search_url = self.search_url + title
            page = await self.get(search_url)
        except (OSError, asyncio.TimeoutError):
            self.log.error('Cannot reach server at %s', search_url)
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
