import pytest

import bs4

from mariner.proxies import piratebay


class TestPirateBayProxy:

    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert isinstance(proxy, str)
        assert 'http' in proxy

    def test_is_online(self, engine):
        online = bs4.BeautifulSoup(
            '<td class="status"><img alt="up" src="assets/img/up.png"></td>', 'lxml')
        assert engine._is_online(online) == True

    def test_is_offline(self, engine):
        offline = bs4.BeautifulSoup(
            '<td class="status"><img alt="up" src="assets/img/down.png"></td>', 'lxml')
        assert engine._is_online(offline) == False

    def test_no_proxy_list(self, engine, monkeypatch, event_loop):
        async def no_results(*args, **kwargs):
            return ''
        monkeypatch.setattr(piratebay.PirateBayProxy, 'get', no_results)
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert proxy == engine.default_proxy

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return PirateBay instance."""
        async def mock_get(*args, **kwargs):
            return """
            <table><tr></tr>
            <tr><td class="site"><a rel="nofollow" class="t1" href="https://pirateproxy.sh">pirateproxy.sh <img src="assets/img/secure.gif" width="16" height="16"></a></td><td class="country"><img src="assets/img/flags/uk.gif" alt="uk" title="uk"></td><td class="status"><img alt="up" src="assets/img/up.png"></td><td class="speed"><span title="Loaded in 1.112 seconds">Very Fast</span></td><td class="report"><a href="#" onclick="reportLink('pirateproxy.sh')" title="Report this proxy"><img src="assets/img/attention.png" alt="Report this proxy"></a></td></tr>
            </tr>
                """
        monkeypatch.setattr(piratebay.PirateBayProxy, 'get', mock_get)
        return piratebay.PirateBayProxy()
