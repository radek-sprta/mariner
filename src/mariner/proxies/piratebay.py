"""Handle PirateBay alternative proxies."""
import bs4

from mariner import exceptions, proxyplugin


class PirateBayProxy(proxyplugin.ProxyPlugin):
    """PirateBay proxy list."""
    proxy_page_url = 'https://proxybay.github.io'

    @staticmethod
    def _parse(page: str) -> str:
        """Parse the page and return a list of pages.

        Args:
            page: Proxy list page to parse.

        Returns:
            Urls of proxy websites.
        """
        soup = bs4.BeautifulSoup(page, 'lxml')
        data = soup.select('table')[0].select('tr')[1:]

        for site in data:
            if PirateBayProxy._is_online(site):
                return site.select('td.site')[0].a.get('href')

        raise exceptions.NoProxyAvailable('No proxy available for PirateBay')

    @staticmethod
    def _is_online(soup: bs4.Tag) -> bool:
        """Check if proxy is online or not.

        Args:
            soup: BeautifulSoup for Proxy data.

        Returns:
            True if site is listed online."""
        status = soup.select('td.status')[0].img.get('src')
        return True if 'up' in status else False
