import pytest

from .context import mariner
from mariner import searchengine, torrent
from mariner.plugins import tokyotosho


class TestTokyoTosho:
    """
    Class to test TokyoTosho plugin.
    """

    def test_tokyotosho_search_url_is_string(self):
        """Search url class attribute is string."""
        assert isinstance(tokyotosho.TokyoTosho.search_url, str)

    def test_results(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('Ubuntu'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return TokyoTosho instance."""
        async def mock_get(*args, **kwargs):
            return """
<tr class="shade category_0"><td rowspan="2"><a href="/?cat=5"><span class="sprite_cat-other"></span></a></td><td class="desc-top"><a href="magnet:?xt=urn:btih:4UBTDIFIJGOZL34OXVKGCE6NAIJHLSDX&amp;tr=http%3A%2F%2Ftorrent.ubuntu.com%3A6969%2Fannounce&amp;tr=http%3A%2F%2Fipv6.torrent.ubuntu.com%3A6969%2Fannounce"><span class="sprite_magnet"></span></a> <a href="http://releases.ubuntu.com/13.04/ubuntu-13.04-server-amd64.iso.torrent" rel="nofollow" type="application/x-bittorrent">ubuntu-13.<span class="s"> </span>04-server-amd64.<span class="s"> </span>iso</a></td><td class="web"><a href="details.php?id=647647" rel="nofollow">Details</a></td></tr>
<tr class="shade category_0"><td class="desc-bot">Submitter: Anonymous | Size: 701MB | Date: 2013-04-25 11:34 UTC</td><td align="right" class="stats" style="color: #BBB; font-family: monospace">S: <span style="color: red">0</span> L: <span style="color: red">0</span> C: <span style="color: red">0</span> ID: 647647</td></tr>
<tr class="category_0"><td rowspan="2"><a href="/?cat=5"><span class="sprite_cat-other"></span></a></td><td class="desc-top"><a href="magnet:?xt=urn:btih:3KWHACHC4OTOIMQZKDATC2IKZIQMLIEK&amp;tr=http%3A%2F%2Ftorrent.ubuntu.com%3A6969%2Fannounce&amp;tr=http%3A%2F%2Fipv6.torrent.ubuntu.com%3A6969%2Fannounce"><span class="sprite_magnet"></span></a> <a href="http://releases.ubuntu.com/13.04/ubuntu-13.04-desktop-i386.iso.torrent" rel="nofollow" type="application/x-bittorrent">ubuntu-13.<span class="s"> </span>04-desktop-i386.<span class="s"> </span>iso</a></td><td class="web"><a href="details.php?id=647646" rel="nofollow">Details</a></td></tr>
<tr class="category_0"><td class="desc-bot">Submitter: Anonymous | Size: 794MB | Date: 2013-04-25 11:33 UTC</td><td align="right" class="stats" style="color: #BBB; font-family: monospace">S: <span style="color: red">0</span> L: <span style="color: red">0</span> C: <span style="color: red">0</span> ID: 647646</td></tr>
<tr class="shade category_0"><td rowspan="2"><a href="/?cat=7"><span class="sprite_cat-raw"></span></a></td><td class="desc-top"><a href="magnet:?xt=urn:btih:C2XTZE5IIQTKTIKMZHXBVKALTT26PDZX&amp;tr=http%3A%2F%2Ftorrent.ubuntu.com%3A6969%2Fannounce"><span class="sprite_magnet"></span></a> <a href="http://cdimage.ubuntu.com/ubuntustudio/releases/12.04/release/ubuntustudio-12.04-dvd-amd64.iso.torrent" rel="nofollow" type="application/x-bittorrent">ubuntustudio-12.<span class="s"> </span>04-dvd-amd64.<span class="s"> </span>iso</a></td><td class="web"><a href="details.php?id=547389" rel="nofollow">Details</a></td></tr>
<tr class="shade category_0"><td class="desc-bot">Submitter: Anonymous | Size: 1.92GB | Date: 2012-07-14 17:11 UTC</td><td align="right" class="stats" style="color: #BBB; font-family: monospace">S: <span style="color: red">0</span> L: <span style="color: red">0</span> C: <span style="color: red">0</span> ID: 547389</td></tr>

                """
        monkeypatch.setattr(tokyotosho.TokyoTosho, 'get', mock_get)
        return tokyotosho.TokyoTosho()
