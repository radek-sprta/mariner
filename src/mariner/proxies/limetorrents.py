"""Handle LimeTorrents alternative proxies."""
import bs4

from mariner import exceptions, proxyplugin


class LimeTorrentsProxy(proxyplugin.ProxyPlugin):
    """LimeTorrents proxy list."""
    proxy_page_url = 'https://limetorrents-proxy.ga/'

    @staticmethod
    def _parse(page: str) -> str:
        """Parse the page and return a list of pages.

        Args:
            page: Proxy list page to parse.

        Returns:
            Urls of proxy websites.
        """
        soup = bs4.BeautifulSoup(page, 'lxml')
        data = soup.select('table.proxy-list')[0].select('tr')[1:]

        for site in data:
            if LimeTorrentsProxy._is_online(site):
                return site.select('td.plc-1')[0].a.get('href')

        raise exceptions.NoProxyAvailable(
            'No proxy available for LimeTorrents')

    @staticmethod
    def _is_online(soup: bs4.Tag) -> bool:
        """Check if proxy is online or not.

        Args:
            soup: BeautifulSoup for Proxy data.

        Returns:
            True if site is listed online."""
        status = soup.select('span.label')[0].string
        return True if 'Online' in status else False
