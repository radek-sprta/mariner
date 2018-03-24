"""Handle KickAssTorrents alternative proxies."""
import bs4

from mariner import exceptions, proxyplugin


class KickAssTorrentsProxy(proxyplugin.ProxyPlugin):
    """KickAssTorrents proxy list."""
    proxy_page_url = 'https://kickassproxy.eu'

    @staticmethod
    def _parse(page: str) -> str:
        """Parse the page and return a list of pages.

        Args:
            page: Proxy list page to parse.

        Returns:
            Urls of proxy websites.
        """
        soup = bs4.BeautifulSoup(page, 'lxml')
        data = soup.select('table.table-striped')[0].select('tr')[1:]

        for site in data:
            if KickAssTorrentsProxy._is_online(site):
                return site.select('td.text-left')[0].a.get('href')

        raise exceptions.NoProxyAvailable(
            'No proxy available for KickAssTorrents')

    @staticmethod
    def _is_online(soup: bs4.Tag) -> bool:
        """Check if proxy is online or not.

        Args:
            soup: BeautifulSoup for Proxy data.

        Returns:
            True if site is listed online."""
        status = soup.select('span.label')[0].string
        return True if 'Online' in status else False
