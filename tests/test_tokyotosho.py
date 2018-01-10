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

    def test_search(self, engine):
        """Search returns an iterator of Torrent objects."""
        search = engine.search('Kino')
        assert isinstance(search, list)
        assert isinstance(search[0], torrent.Torrent)

    @pytest.mark.parametrize('limit', [1, 2, 3])
    def test_search_limit(self, engine, limit):
        """Get results should get number of URLs up to a limit."""
        search = engine.search('Kino', limit)
        assert len(search) == limit

    def test_search_limit_zero(self, engine):
        """Get results should throw ValueError when limit is zero."""
        with pytest.raises(ValueError):
            engine.search('Kino', limit=0)

    def test_get_torrent(self, engine):
        """Return torrent with given ID."""
        engine.search('Kino')
        assert isinstance(engine.get_torrent(1), torrent.Torrent)

    @pytest.mark.parametrize('tid', [-1, -9999, 10000])
    def test_get_torrent_non_existant(self, engine, tid):
        engine.search('Kino')
        with pytest.raises(searchengine.NoResultException):
            engine.get_torrent(tid)

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return TokyoTosho instance."""
        async def mock_get(*args, **kwargs):
            return """
<html>
 <body>
  <td class="desc-top">
   <a href="magnet:?xt=urn:btih:FM5JTPJ7Q77DCABUJTU25MZASYWMUUVC&amp;tr=udp%3A%2F%2Fa.leopard-raws.org%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&$
mp;tr=udp%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&amp;tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&amp;tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce">
    <span class="sprite_magnet">
    </span>
   </a>
   <a href="http://jp.leopard-raws.org/download.php?hash=9298148996e6fd9265baae8202325759" rel="nofollow" type="application/x-bittorrent">
    [Leopard-Raws] Kino no Tabi - The Beautiful World - Animated Series - 12 END (ATX 1280x720 x264 AAC).
    <span class="s">
    </span>
    mp4
   </a>
  </td>
  <td class="web">
   <a href="details.php?id=1172358" rel="nofollow">
    Details
   </a>
  </td>
  <tr class="shade category_0">
   <td class="desc-bot">
    Authorized:
    <span class="auth_bad">
     No
    </span>
    Submitter: Anonymous | Size: 442.62MB | Date: 2017-12-31 03:31 UTC
   </td>
   <td align="right" class="stats" style="color: #BBB; font-family: monospace">
    S:
    <span style="color: red">
     0
    </span>
    L:
    <span style="color: red">
     0
    </span>
    C:
    <span style="color: red">
     0
    </span>
    ID: 1172358
   </td>
  </tr>
  <tr class="category_0">
   <td rowspan="2">
    <a href="/?cat=10">
     <span class="sprite_cat-noneng">
     </span>
    </a>
   </td>
  <td class="desc-top">
    <a href="magnet:?xt=urn:btih:LYGTL3664YUJFYFJDIT5CDWDBVQ6EYHL&amp;tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&amp;tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&amp;tr=udp%3A
%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce">
     <span class="sprite_magnet">
     </span>
    </a>
    <a href="https://nyaa.si/download/992286.torrent" rel="nofollow" type="application/x-bittorrent">
     [EA]Kino_no_Tabi_2017_11_[1280x720][HDTV][Hi10p][FD41535E].mkv
    </a>
   </td>
   <td class="web">
    <a href="http://eternalanimes.org/">
     Website
    </a>
    |
    <a href="details.php?id=1172280" rel="nofollow">
     Details
    </a>
   </td>
  </tr>
  <tr class="category_0">
   <td class="desc-bot">
    Submitter:
    <a href="?username=EternalAnimes">
     EternalAnimes
    </a>
    | Size: 159.07MB | Date: 2017-12-30 22:14 UTC | Comment: PT-BR by Eternal Animes.
   </td>
   <td align="right" class="stats" style="color: #BBB; font-family: monospace">
    S:
    <span style="color: orange">
     3
    </span>
   L:
    <span style="color: red">
     0
    </span>
    C:
    <span style="color: red">
     0
    </span>
    ID: 1172280
   </td>
  </tr>
  <tr class="shade category_0">
   <td rowspan="2">
    <a href="/?cat=10">
     <span class="sprite_cat-noneng">
     </span>
    </a>
   </td>
   <td class="desc-top">
    <a href="magnet:?xt=urn:btih:5F3WRQOWL3OYXEDBUE35MHRKVJWD7KER&amp;tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&amp;tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&amp;tr=udp%3A
%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce">
     <span class="sprite_magnet">
     </span>
    </a>
    <a href="https://nyaa.si/download/990294.torrent" rel="nofollow" type="application/x-bittorrent">
     [EA]Kino_no_Tabi_2017_10_[1280x720][HDTV][Hi10p][E462FED5].mkv
    </a>
   </td>
   <td class="web">
    <a href="http://eternalanimes.org/">
     Website
    </a>
   |
    <a href="details.php?id=1169816" rel="nofollow">
     Details
    </a>
   </td>
  </tr>
  <tr class="shade category_0">
   <td class="desc-bot">
    Submitter:
    <a href="?username=EternalAnimes">
     EternalAnimes
    </a>
    | Size: 216.15MB | Date: 2017-12-23 18:55 UTC | Comment: PT-BR by Eternal Animes.
   </td>
   <td align="right" class="stats" style="color: #BBB; font-family: monospace">
    S:
    <span style="color: green">
     6
    </span>
    L:
    <span style="color: red">
     0
    </span>
    C:
    <span style="color: red">
     0
    </span>
    ID: 1169816
   </td>
  </tr>
  <tr class="category_0">
   <td rowspan="2">
    <a href="/?cat=1">
     <span class="sprite_cat-anime">
     </span>
    </a>
   </td>
  </tr>
 </body>
</html>
                """
        monkeypatch.setattr(tokyotosho.TokyoTosho, 'get', mock_get)
        return tokyotosho.TokyoTosho()
