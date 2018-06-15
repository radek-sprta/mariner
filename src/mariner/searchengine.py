# -*- coding: future_fstrings -*-
"""Handle searching for torrents on torrent trackers."""
import asyncio
import importlib
import inspect
import itertools
import logging
import pathlib
from typing import List, Iterator, Optional, Tuple, Union

import cachalot
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from mariner import exceptions, torrent

Name = str
Page = str
Path = Union[str, pathlib.Path]
Url = str


class SearchEngine:
    """Search on for a torrent using Tracker plugins."""

    log = logging.getLogger(__name__)
    plugin_directory = pathlib.Path(__file__).parent / 'trackers'

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.plugins = {}
        self.results = cachalot.Cache(
            path='~/.local/share/mariner/results.json', size=1000)
        self.initialize_plugins()

    @property
    def timeout(self) -> int:
        "Timeout for connections."
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        if timeout <= 0:
            raise exceptions.ConfigurationError('Timeout cannot be negative.')
        self._timeout = timeout  # pylint: disable=attribute-defined-outside-init

    @staticmethod
    def _flatten(nested_list: List[List]) -> List:
        """Flatten a list."""
        return list(itertools.chain(*nested_list))

    def _load_modules(self) -> Iterator:
        """Find and import tracker plugins."""
        for module in self.plugin_directory.glob('*.py'):  # pylint: disable=no-member
            # Cast to str as a workaround for Python 3.5
            name = str(module.stem)
            module = str(module)

            self.log.debug('Loading module=%s', module)
            spec = importlib.util.spec_from_file_location(name, module)
            loaded_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded_module)
            yield loaded_module

    def initialize_plugins(self) -> None:
        """Find engines and register them."""
        self.log.debug('Initializing plugins')
        for module in self._load_modules():
            classes = inspect.getmembers(module, inspect.isclass)
            for name, plugin in classes:
                # We don't care about classes defined in other modules
                if not plugin.__module__ == module.__name__:
                    continue
                self.log.debug('Adding plugin=%s', plugin)
                self.plugins[name.lower()] = plugin
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
                       trackers: List[str]) -> List[torrent.Torrent]:
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
            raise exceptions.ConfigurationError(
                "Illegal value for default_tracker")
        else:
            tasks = asyncio.gather(
                *(p(timeout=self.timeout).results(title.lower()) for p in plugins))
            loop = asyncio.get_event_loop()
            torrents = loop.run_until_complete(tasks)
            torrents = self._flatten(torrents)
        return torrents

    def search(self,  # pylint: disable=too-many-arguments
               title: str,
               trackers: List[str],
               limit: Optional[int] = 10,
               sort_by_newest: bool = False) -> List[Tuple[int, torrent.Torrent]]:
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
        sorted_torrents = self._sort_results(torrents, sort_by_newest)

        # Show only results up to to the limit
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

    def _sort_results(self,
                      torrents: List[torrent.Torrent],
                      sort_by_newest: bool) -> List[torrent.Torrent]:
        """Sort torrent results.

        Args:
            torrents: List of torrents to sort.
            sort_by_newest: True if torrent should be sorted by recendivity.

        Returns:
            Sorted list of torrents.
        """
        self.log.debug('Sorting results')
        if sort_by_newest:
            sorted_torrents = list(
                reversed(sorted(torrents, key=lambda x: x.date)))
        else:
            sorted_torrents = list(reversed(sorted(torrents)))
        return sorted_torrents
