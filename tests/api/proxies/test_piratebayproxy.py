import pytest

import bs4

from mariner.proxies import piratebay


class TestPirateBayProxy:
    @pytest.mark.vcr()
    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert isinstance(proxy, str)
        assert "http" in proxy

    def test_is_online(self, engine):
        online = bs4.BeautifulSoup(
            '<td class="status"><img alt="up" src="assets/img/up.png"></td>', "lxml"
        )
        assert engine._is_online(online) == True

    def test_is_offline(self, engine):
        offline = bs4.BeautifulSoup(
            '<td class="status"><img alt="up" src="assets/img/down.png"></td>', "lxml"
        )
        assert engine._is_online(offline) == False

    def test_no_proxy_list(self, engine, monkeypatch, event_loop):
        async def no_results(*args, **kwargs):
            return ""

        monkeypatch.setattr(piratebay.PirateBayProxy, "get", no_results)
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert proxy == engine.default_proxy

    @pytest.fixture(scope="module")
    def engine(self):
        """Return PirateBay instance."""
        return piratebay.PirateBayProxy()
