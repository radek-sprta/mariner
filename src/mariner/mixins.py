"""Utility mixins used in Mariner."""
import aiohttp
import async_timeout


class ComparableMixin:  # pylint: disable=too-few-public-methods
    """Implement comparisons, using _cmpkey attribute."""

    def _compare(self, other, method):
        """Wrap rich comparison methods.

        Args:
            other: Object to compare to.
            method: Comparison method to use.

        Returns:
            Comparison function.
        """
        try:
            return method(self._cmpkey, other._cmpkey)  # pylint: disable=protected-access
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or returned different type,
            # so cannot make a comparison with "other".
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)


class GetPageMixin:  # pylint: disable=too-few-public-methods
    """Represent a web scraper."""

    async def get(self, url: str, headers: str = None, cookies: str = None) -> str:
        """Get the requested page.

        Args:
            url: Url of the page to get.

        Returns:
            Raw HTML page.
        """
        with async_timeout.timeout(10):
            async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
                async with session.get(url) as response:
                    return await response.text()
