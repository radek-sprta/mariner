import pytest

import bs4

from mariner.proxies import kickasstorrents


class TestKickAssTorrentsProxy:

    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert isinstance(proxy, str)
        assert 'http' in proxy

    def test_is_online(self, engine):
        online = bs4.BeautifulSoup(
            '<span class="label label-success">Online</span>', 'lxml')
        assert engine._is_online(online) == True

    def test_is_offline(self, engine):
        offline = bs4.BeautifulSoup(
            '<span class="label label-success">Offline</span>', 'lxml')
        assert engine._is_online(offline) == False

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return KickAssTorrents instance."""
        async def mock_get(*args, **kwargs):
            return """
            <table class="table table-bordered table-striped table-hover">
            <tr></tr>
            <tr>
            <td class="text-left"> <img src="./kickassproxy/kickass_proxy.png" title="Kickass Proxy" alt="Kickass Proxy"> &nbsp;&nbsp;&nbsp;<a target="_blank" href="https://kickasstorrents.pw/">kickasstorrents.pw</a>
            </td>
            <td class="text-center" title="72.0 ms"><span class="label label-success">Online</span>
            </td>
            </tr>
            </table>
                """
        monkeypatch.setattr(
            kickasstorrents.KickAssTorrentsProxy, 'get', mock_get)
        return kickasstorrents.KickAssTorrentsProxy()
