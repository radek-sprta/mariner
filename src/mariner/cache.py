"""Persistent memoization using TinyDB."""
import functools
import hashlib
from typing import Any, Callable, Dict

import jsonpickle
import pendulum  # pylint: disable=wrong-import-order
import tinydb  # pylint: disable=wrong-import-order
import tinydb_smartcache

from mariner import utils


class Cache:
    """Offline cache for search results.

    Attributes:
        path: Path to the database file.
        timeout: Defaults to 1 day. Period after which results should expire.
        size: Defaults to 10000. Maximum number of cached results.
        storage: Defaults to JSONStorage. Storage type for TinyDB.
    """

    def __init__(self,
                 *,
                 path: str = '~/.cache/mariner/cache.json',
                 timeout: int = 86400,
                 size: int = 10000,
                 storage: tinydb.storages.Storage = tinydb.storages.JSONStorage,
                 ) -> None:  # pylint: disable=bad-continuation
        self.path = utils.check_path(path)
        self.timeout = timeout
        self.size = size
        self.db = tinydb.TinyDB(self.path, storage)
        self.db.table_class = tinydb_smartcache.SmartCacheTable

    def clear(self) -> None:
        """Clear the cache."""
        self.db.purge()

    def expiry(self) -> pendulum.Pendulum:
        """Return expiration time for cached results."""
        expiry = pendulum.now().add(seconds=self.timeout)
        return self._serialize_date(expiry)

    def get(self, key: str) -> Any:
        """Get torrent from database.

        Args:
            key: Key hash.

        Returns:
            Cached object.
        """
        self._remove_expired()
        entry = tinydb.Query()
        value = self.db.get(entry.key == key)
        if value:
            self.db.update({'time': self.expiry()}, entry.key == key)
            return jsonpickle.decode(value['value'])
        return None

    def insert(self, key: str, entry: Any) -> None:
        """Insert entry into cache.

        Args:
            key: Key hash of the entry to store.
            entry: Object to cache.
        """
        value = jsonpickle.encode(entry)
        self.db.insert({'key': key, 'time': self.expiry(), 'value': value})
        if len(self.db) > self.size:
            self._remove_oldest()

    def remove(self, key: str) -> None:
        """Delete key from cache.

        Args:
            key: Hash key to delete from the cache.
        """
        entry = tinydb.Query()
        self.db.remove(entry.key == key)

    def _remove_expired(self) -> None:
        """Remove old entries."""
        entry = tinydb.Query()
        now = self._serialize_date(pendulum.now())
        self.db.remove(entry.time < now)

    def _remove_oldest(self) -> None:
        """Remove oldest entry."""
        oldest = self.db.all()[0].key
        self.remove(oldest)

    @staticmethod
    def _serialize_date(date: pendulum.Pendulum) -> Dict[str, str]:
        """Serialize date so it can be stored in database.

        Args:
            date: Date to serialize.

        Returns:
            Serialized date.
        """
        return jsonpickle.encode(date)

    def __call__(self, function: Callable[..., Any]):
        """Decorator for caching function results.

        Args:
            function: Function to decorate.

        Returns:
            Cached function.
        """
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            """Cache function."""
            result = ''
            seed = function.__name__ + \
                jsonpickle.encode(args) + jsonpickle.encode(kwargs)
            key = hashlib.md5(seed.encode('utf8')).hexdigest()
            result = self.get(key)
            if not result:
                result = function(*args, **kwargs)
                self.insert(key, result)
            return result
        return wrapped
