import pytest

import bs4

from mariner.proxies import limetorrents


class TestLimeTorrentsProxy:

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
        """Return LimeTorrents instance."""
        async def mock_get(*args, **kwargs):
            return """
	    <table class="table table-striped proxy-list mt20">
            <tr></tr>
	    <tr class="pl-item bg-warning">
            <td class="plc-1"><a target="_blank" href="https://limetorrents.mrunlock.stream" title="limetorrents.mrunlock.stream"><i class="fa fa-link mr5"></i>limetorrents.mrunlock.stream</a></td>
            <td class="plc-2"><img src="/images/premium.png" class="flag-i" title="Featured" alt="Featured">Featured</td>
            <td class="plc-3"><a href="https://upordown.info/status/limetorrents.cc" title="Check LimeTorrents Status" target="_blank"><span class="label label-success">Online</span></a></td>
            <td class="plc-4"><a href="/qr/limetorrents.mrunlock.stream" title="Scan QR Code for limetorrents.mrunlock.stream"><i class="fa fa-qrcode"></i></a> <a href="mailto:unblocked@cock.lu?subject=report_limetorrents.mrunlock.stream" title="Broken link? Report it to our staff"><i class="fa fa-warning"></i></a></td>
            </tr>
            </table>
                """
        monkeypatch.setattr(
            limetorrents.LimeTorrentsProxy, 'get', mock_get)
        return limetorrents.LimeTorrentsProxy()
