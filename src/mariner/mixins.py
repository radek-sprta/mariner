"""Utility mixins used in Mariner."""
from typing import Dict, Union

import aiohttp


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


class RequestMixin:  # pylint: disable=too-few-public-methods
    """Mixin for HTTP requests."""

    user_agent = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
    }

    async def get(
        self,
        url: str,
        *,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None,
        timeout: int = None
    ) -> str:
        """Get the requested page.

        Args:
            url: Url of the page to get.
            headers: Request headers.
            cookies: Request cookies.
            timeout: Request timeout.

        Returns:
            Raw HTML page.
        """
        return await self.request("get", url, headers=headers, cookies=cookies, timeout=timeout)

    async def request(
        self,
        method: str,
        url: str,
        *,
        data: Union[Dict, bytes] = None,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None,
        timeout: int = 10
    ) -> str:
        """Make a request.

        Args:
            method: Request method.
            url: Url of the page.
            data: Request payload.
            headers: Request headers.
            cookies: Request cookies.
            timeout: Request timeout.

        Returns:
            HTTP response.
        """
        headers = {**headers, **self.user_agent} if headers else self.user_agent

        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            async with session.request(method, url, data=data, timeout=timeout) as response:
                return await response.text()
