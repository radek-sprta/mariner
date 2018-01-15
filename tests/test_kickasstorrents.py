import pytest

from .context import mariner
from mariner import torrent
from mariner.plugins import kickasstorrents


class TestKickAssTorrents:
    """
    Class to test KickAssTorrents plugin.
    """

    def test_kickasstorrents_search_url_is_string(self):
        """Search url class attribute is string."""
        assert isinstance(kickasstorrents.KickAssTorrents.search_url, str)

    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('Ubuntu'))
        assert isinstance(search, list)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return KickAssTorrents instance."""
        async def mock_get(*args, **kwargs):
            return """
<tbody><tr> <td> <div class="torrents_table__torrent_name"> <i class="torrents_table__media_icon kf__file"></i> <div class="text--left"> <a class="torrents_table__torrent_title" href="https://katcr.co/torrent/177934/lynda-lfcs-user-and-group-management-ubuntu.html"><b>Lynda - LFCS User and Group Management (Ubuntu)</b></a>
<span class="torrents_table__upload_info"> Posted by <span class="user_badge acl_123"> <i class="kf__crown text--verified"></i> <a href="https://katcr.co/user/KATutorials/page/1/uploads/">KATutorials</a>
</span> in <a href="https://katcr.co/category/other.html" class="text--muted"><strong>Other</strong></a> &gt; <a href="https://katcr.co/cat/other/sub/tutorials/page/1.html" class="text--muted"> <strong>Tutorials</strong></a> </span> </div> <div class="torrents_table__actions"> <a class="button button--small" href="" title="Comments">0 <i class="kf__comment"></i></a> <a class="button button--small button--green" href="" title="Verified torrent"><i class="kf__crown"></i></a> <a class="button button--small" href="magnet:?xt=urn:btih:227dc77a394abab85df1f3095e35d96649c2f469&amp;dn=Lynda+-+LFCS++User+and+Group+Management+%28Ubuntu%29&amp;xl=175566842&amp;tr=udp://tracker.leechers-paradise.org:6969/announce&amp;tr=udp://tracker.zer0day.to:1337/announce&amp;tr=udp://glotorrents.pw:6969/announce&amp;tr=udp://tracker.pubt.net:2710/announce&amp;tr=udp://tracker.openbittorrent.com:80/announce&amp;tr=udp://open.demonii.com:1337/announce&amp;tr=udp://coppersurfer.tk:6969/announce" title="Torrent magnet link"><i class="kf__magnet"></i></a></div></div></td><td class="text--nowrap text--center" data-title="Size">167.43 MB</td><td class="text--nowrap text--center" data-title="Files">15</td><td class="text--nowrap text--center" data-title="Age" title="2017-09-25 09:37:10">4 months ago</td><td class="text--nowrap text--center text--success" data-title="Seed">2</td><td class="text--nowrap text--center text--error" data-title="Leech">1</td></tr><tr> <td> <div class="torrents_table__torrent_name"> <i class="torrents_table__media_icon kf__book"></i> <div class="text--left"> <a class="torrents_table__torrent_title" href="https://katcr.co/torrent/168887/ubuntu-16-04-the-complete-manual-2016.html"><b>Ubuntu 16 04, The Complete Manual - 2016</b></a>
<span class="torrents_table__upload_info"> Posted by <span class="user_badge acl_123"> <i class="kf__crown"></i> <a href="https://katcr.co/user/Praniya2/page/1/uploads/">Praniya2</a>
</span> in <a href="https://katcr.co/category/books.html" class="text--muted"><strong>Books</strong></a> &gt; <a href="https://katcr.co/cat/books/sub/magazines/page/1.html" class="text--muted"> <strong>Magazines</strong></a> </span> </div> <div class="torrents_table__actions"> <a class="button button--small" href="" title="Comments">0 <i class="kf__comment"></i></a> <a class="button button--small" href="magnet:?xt=urn:btih:6afce4771b86ea36ebcc56b8399c9878d87d25d3&amp;dn=Ubuntu+16.04%2C+The+Complete+Manual+-+2016&amp;xl=50058840&amp;tr=udp://tracker.coppersurfer.tk:6969/announce&amp;tr=udp://tracker.coppersurfer.tk:6969&amp;tr=udp://tracker.opentrackr.org:1337/announce&amp;tr=udp://9.rarbg.me:2720/announce&amp;tr=udp://9.rarbg.to:2770/announce&amp;tr=udp://tracker.ilibr.org:6969/announce&amp;tr=udp://tracker.ilibr.org:80/announce&amp;tr=udp://p4p.arenabg.com:1337/announce&amp;tr=udp://p4p.arenabg.ch:1337/announce&amp;tr=udp://eddie4.nl:6969/announce&amp;tr=udp://tracker.leechers-paradise.org:6969/announce&amp;tr=udp://tracker.zer0day.to:1337/announce&amp;tr=udp://shadowshq.yi.org:6969/announce&amp;tr=udp://tracker.filetracker.pl:8089/announce&amp;tr=udp://ipv4.tracker.harry.lu:80/announce" title="Torrent magnet link"><i class="kf__magnet"></i></a></div></div></td><td class="text--nowrap text--center" data-title="Size">47.74 MB</td><td class="text--nowrap text--center" data-title="Files">1</td><td class="text--nowrap text--center" data-title="Age" title="2017-09-11 01:38:58">4 months ago</td><td class="text--nowrap text--center text--success" data-title="Seed">8</td><td class="text--nowrap text--center text--error" data-title="Leech">0</td></tr><tr> <td> <div class="torrents_table__torrent_name"> <i class="torrents_table__media_icon kf__file"></i> <div class="text--left"> <a class="torrents_table__torrent_title" href="https://katcr.co/torrent/123524/lynda-building-an-ubuntu-home-server.html"><b>Lynda - Building an Ubuntu Home Server</b></a>
<span class="torrents_table__upload_info"> Posted by <span class="user_badge acl_123"> <i class="kf__crown text--verified"></i> <a href="https://katcr.co/user/back2reverse/page/1/uploads/">back2reverse</a>
</span> in <a href="https://katcr.co/category/other.html" class="text--muted"><strong>Other</strong></a> &gt; <a href="https://katcr.co/cat/other/sub/tutorials/page/1.html" class="text--muted"> <strong>Tutorials</strong></a> </span> </div> <div class="torrents_table__actions"> <a class="button button--small" href="" title="Comments">0 <i class="kf__comment"></i></a> <a class="button button--small button--green" href="" title="Verified torrent"><i class="kf__crown"></i></a> <a class="button button--small" href="magnet:?xt=urn:btih:d86c7c89d47689a55298b2b54e00f00444b52a4a&amp;dn=Lynda+-+Building+an+Ubuntu+Home+Server&amp;xl=400198391&amp;tr=http://bt3.t-ru.org/ann?pk=24f63de2304d9bedd4e7a24dff264d37&amp;tr=http://retracker.local/announce&amp;tr=udp://tracker.coppersurfer.tk:6969/announce&amp;tr=udp://tracker.pirateparty.gr:6969/announce&amp;tr=udp://tracker.opentrackr.org:1337/announce&amp;tr=udp://eddie4.nl:6969/announce&amp;tr=udp://shadowshq.yi.org:6969/announce&amp;tr=udp://tracker.leechers-paradise.org:6969&amp;tr=udp://tracker.zer0day.to:1337/announce&amp;tr=udp://p4p.arenabg.com:1337/announce&amp;tr=udp://thetracker.org:80/announce&amp;tr=udp://9.rarbg.me:2710/announce&amp;tr=udp://9.rarbg.com:2710/announce&amp;tr=udp://9.rarbg.to:2710/announce&amp;tr=udp://inferno.demonoid.pw:3395/announce" title="Torrent magnet link"><i class="kf__magnet"></i></a></div></div></td><td class="text--nowrap text--center" data-title="Size">381.66 MB</td><td class="text--nowrap text--center" data-title="Files">29</td><td class="text--nowrap text--center" data-title="Age" title="2017-06-16 01:29:05">7 months ago</td><td class="text--nowrap text--center text--success" data-title="Seed">8</td><td class="text--nowrap text--center text--error" data-title="Leech">1</td></tr><tr></tbody>
                """
        monkeypatch.setattr(kickasstorrents.KickAssTorrents, 'get', mock_get)
        return kickasstorrents.KickAssTorrents()
