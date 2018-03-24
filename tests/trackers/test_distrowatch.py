import pytest

from mariner import torrent
from mariner.trackers import distrowatch


class TestDistrowatch:
    """
    Class to test Distrowatch plugin.
    """

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return Distrowatch instance."""
        async def mock_get(*args, **kwargs):
            return """
                <table cellpadding="5"><tr><th></th></tr>
                <tr><td class=torrent><a href="dwres/torrents/ubuntu-16.04.3-desktop-amd64.iso.torrent">ubuntu-16.04.3-desktop-amd64.iso.torrent</a></td>
                <td class=torrentdate align=center>2017-08-05</td>
                </tr>
                <tr><td class=torrent><a href="dwres/torrents/netrunner-1706-64bit.iso.torrent">netrunner-1706-64bit.iso.torrent</a></td>
                <td class=torrentdate align=center>2017-07-01</td>
                </tr>
                <tr><td class=torrent><a href="dwres/torrents/lubuntu-17.10-alpha1-amd64.iso.torrent">lubuntu-17.10-alpha1-amd64.iso.torrent</a></td>
                <td class=torrentdate align=center>2017-07-01</td>
                </tr>
                <tr><td class=torrent><a href="dwres/torrents/kubuntu-17.10-alpha1-amd64.iso.torrent">kubuntu-17.10-alpha1-amd64.iso.torrent</a></td>
                <td class=torrentdate align=center>2017-07-01</td>
                </table>
                """
        monkeypatch.setattr(distrowatch.Distrowatch, 'get', mock_get)
        return distrowatch.Distrowatch()

    def test_results(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('ubuntu'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3
