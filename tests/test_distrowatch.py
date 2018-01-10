import pytest

from .context import mariner
from mariner import searchengine, torrent
from mariner.plugins import distrowatch


class TestDistrowatch:
    """
    Class to test Distrowatch plugin.
    """

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return Distrowatch instance."""
        async def mock_get(*args, **kwargs):
            return """
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
                """
        monkeypatch.setattr(distrowatch.Distrowatch, 'get', mock_get)
        return distrowatch.Distrowatch()

    def test_distrowatch_search_url_is_string(self):
        """Search url class attribute is string."""
        assert isinstance(distrowatch.Distrowatch.search_url, str)

    def test_search(self, engine):
        """Search returns an iterator of Torrent objects."""
        search = engine.search('Ubuntu')
        assert isinstance(search, list)
        assert isinstance(search[0], torrent.Torrent)

    def test_search_non_existant(self, engine):
        """Search for non existing string should return NoResultException."""
        with pytest.raises(searchengine.NoResultException):
            engine.search('ZXCVB')

    @pytest.mark.parametrize('limit', [1, 2, 3])
    def test_search_limit(self, engine, limit):
        """Get results should get number of URLs up to a limit."""
        search = engine.search('Ubuntu', limit)
        assert len(search) == limit

    def test_search_limit_zero(self, engine):
        """Get results should throw ValueError when limit is zero."""
        with pytest.raises(ValueError):
            engine.search('Ubuntu', limit=0)

    def test_get_torrent(self, engine):
        """Return torrent with given ID."""
        engine.search('Ubuntu')
        assert isinstance(engine.get_torrent(1), torrent.Torrent)

    @pytest.mark.parametrize('tid', [-1, -9999, 10000])
    def test_get_torrent_non_existant(self, engine, tid):
        engine.search('Ubuntu')
        with pytest.raises(searchengine.NoResultException):
            engine.get_torrent(tid)
