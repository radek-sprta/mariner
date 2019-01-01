import pytest

import bs4

from mariner.proxies import limetorrents


class TestLimeTorrentsProxy:
    @pytest.mark.vcr()
    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert isinstance(proxy, str)
        assert "http" in proxy

    def test_is_online(self, engine):
        online = bs4.BeautifulSoup('<span class="label label-success">Online</span>', "lxml")
        assert engine._is_online(online) == True

    def test_is_offline(self, engine):
        offline = bs4.BeautifulSoup('<span class="label label-success">Offline</span>', "lxml")
        assert engine._is_online(offline) == False

    def test_no_proxy_list(self, engine, monkeypatch, event_loop):
        async def no_results(*args, **kwargs):
            return ""

        monkeypatch.setattr(limetorrents.LimeTorrentsProxy, "get", no_results)
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert proxy == engine.default_proxy

    @pytest.fixture(scope="module")
    def engine(self):
        """Return LimeTorrents instance."""
        return limetorrents.LimeTorrentsProxy()
