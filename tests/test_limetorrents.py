import pytest

from .context import mariner
from mariner import torrent
from mariner.plugins import limetorrents


class TestLimeTorrents:
    """
    Class to test LimeTorrents plugin.
    """

    def test_limetorrents_search_url_is_string(self):
        """Search url class attribute is string."""
        assert isinstance(limetorrents.LimeTorrents.search_url, str)

    def test_results(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('Ubuntu'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return LimeTorrents instance."""
        async def mock_get(*args, **kwargs):
            return """

<table class="table2" cellspacing="0" cellpadding="6"><tbody><tr><th class="thleft">
<span style="float:left">Torrent Name</span>
<span style="float:right"><img src="/static/images/comment16.png" alt="Comments" title="Comments">&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<img src="/static/images/vup16.png" alt="Good" title="Good"></span></th>
<th class="thnormal"><a href="/search/all/ubuntu/date/1/">Added</a></th>
<th class="thnormal"><a href="/search/all/ubuntu/size/1/">Size</a></th>
<th class="thnormal"><a href="/search/all/ubuntu/seeds/1/">Seed</a></th>
<th class="thnormal"><a href="/search/all/ubuntu/leechs/1/">Leech</a></th>
<th class="thright">Health</th>
</tr>
<tr bgcolor="#F4F4F4"><td class="tdleft"><div class="tt-name"><a href="http://itorrents.org/torrent/A7FCE1547E307D3211C90470870215920E6909EF.torrent?title=Ubuntu-12-10-Desktop-AMD64" rel="nofollow" class="csprite_dl14"></a><a href="/Ubuntu-12-10-Desktop-AMD64-torrent-2606810.html">Ubuntu 12 10 Desktop AMD64</a></div><div class="tt-options"></div></td><td class="tdnormal">1 Year+ - in Applications</td><td class="tdnormal">584.27 MB</td><td class="tdseed">3,682</td><td class="tdleech">23</td><td class="tdright"><div class="hb10"></div></td></tr>
<tr bgcolor="#FFFFFF"><td class="tdleft"><div class="tt-name"><a href="http://itorrents.org/torrent/B0B81206633C42874173D22E564D293DAEFC45E2.torrent?title=Ubuntu-11-10-Alternate-Amd64-Iso" rel="nofollow" class="csprite_dl14"></a><a href="/Ubuntu-11-10-Alternate-Amd64-Iso-torrent-3410860.html">Ubuntu 11 10 Alternate Amd64 Iso</a></div><div class="tt-options"></div></td><td class="tdnormal">1 Year+ - in Applications</td><td class="tdnormal">139.92 MB</td><td class="tdseed">3,335</td><td class="tdleech">3,288</td><td class="tdright"><div class="hb10"></div></td></tr>
<tr bgcolor="#F4F4F4"><td class="tdleft"><div class="tt-name"><a href="http://itorrents.org/torrent/779241726DEB5492DCE85525ACFC9E81FD06F63F.torrent?title=Ubuntu-12-10-Desktop-Amd64" rel="nofollow" class="csprite_dl14"></a><a href="/Ubuntu-12-10-Desktop-Amd64-torrent-3403857.html">Ubuntu 12 10 Desktop Amd64</a></div><div class="tt-options"></div></td><td class="tdnormal">1 Year+ - in Applications</td><td class="tdnormal">151.68 MB</td><td class="tdseed">3,329</td><td class="tdleech">3,176</td><td class="tdright"><div class="hb10"></div></td></tr>
</table>
            """
        monkeypatch.setattr(limetorrents.LimeTorrents, 'get', mock_get)
        return limetorrents.LimeTorrents()
