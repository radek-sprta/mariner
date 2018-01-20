import pytest

from .context import mariner
from mariner import torrent
from mariner.plugins import linuxtracker


class TestLinuxTracker:
    """
    Class to test LinuxTracker plugin.
    """

    def test_linuxtracker_search_url_is_string(self):
        """Search url class attribute is string."""
        assert isinstance(linuxtracker.LinuxTracker.search_url, str)

    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('Ubuntu'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return LinuxTracker instance."""
        async def mock_get(*args, **kwargs):
            return """
    <table class="lista" width="100%"></table>
    <table class="lista" width="100%"></table>
    <table class="lista" width="100%"></table>
    <table class="lista" width="100%"></table>
<table class="lista" width="100%">
<tr>
<td class="lista" width="125"> </td><td class="lista"></td></tr>
<tr>
<td align="center" class="lista" width="125">
<center><a href="index.php?page=torrents&amp;category=607"><img alt="Xubuntu" border="0" src="http://linuxtracker.org/style/Linuxtracker.New/images/categories/large/xubuntu.png"/></a><
/center><p>
<a href="/torrentimg/noimage.jpg" rel="lightbox" title="view image">
<img src="thumbnail.php?size=150&amp;path=torrentimg/noimage.jpg"/></a><br/>
<a href="index.php?page=torrent-details&amp;id=456cc88a2b56ca09e22495ed6ec33e9d3d504e83"><img src="/images/more_details_icon.png"/></a>
</p></td>
<td class="lista">
<font size="4"><strong><a href="index.php?page=torrent-details&amp;id=456cc88a2b56ca09e22495ed6ec33e9d3d504e83" title="View details: xubuntu-17.10.1-desktop-i386">xubuntu 17 10 1 deskt
op i386</a> (<span style="color:red">Multi.</span>)   </strong></font><br/>
      Xubuntu is a community-developed operating system based on Ubuntu. It comes with Xfce, which is a stable, light and configurable desktop environment.<br/>
<hr/>
<table width="100%">
<tr><td>
<strong>Added On:</strong> 13/01/2018</td><td> </td></tr>
<tr> <td><strong>Size:</strong> 1.23 GB </td><td></td></tr>
<tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=5&amp;by=2">Seeds</a></strong> 62 </td><td></td></tr>
<tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=6&amp;by=2">Leechers</a></strong> 3 </td><td></td></tr>
<tr> <td width="90%"><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=7&amp;by=1">Completed</a></strong> 505 </td><td align="right"><a href="magn
et:?xt=urn:btih:IVWMRCRLK3FATYRESXWW5QZ6TU6VATUD"><img alt="Magnet Link" border="0" src="images/azureus.gif"/></a> <a href="index.php?page=downloadcheck&amp;id=456cc88a2b56ca09e22495ed
6ec33e9d3d504e83"><img alt="torrent" border="0" src="images/download.gif"/></a>
</td></tr>
</table>
<hr/>
<table width="100%">
<tr>
<td>
---</td><td> <a href="index.php?page=userdetails&amp;id=9892">DEMONLORD</a></td><td>  N/A </td><td> N/A<br/></td>
<td align="center" class="lista" style="text-align: center;" width="20">---</td>
<td> <tag:torrents></tag:torrents></td><td><strong>
</strong></td></tr></table>
</td>
</tr>
<tr>
<td align="center" class="lista" width="125">
<center><a href="index.php?page=torrents&amp;category=607"><img alt="Xubuntu" border="0" src="http://linuxtracker.org/style/Linuxtracker.New/images/categories/large/xubuntu.png"/></a><
/center><p>
<a href="/torrentimg/noimage.jpg" rel="lightbox" title="view image">
<img src="thumbnail.php?size=150&amp;path=torrentimg/noimage.jpg"/></a><br/>
<a href="index.php?page=torrent-details&amp;id=66d0693b9efd7ead162a9beec24089d574d1a2fb"><img src="/images/more_details_icon.png"/></a>
</p></td>
<td class="lista">
<font size="4"><strong><a href="index.php?page=torrent-details&amp;id=66d0693b9efd7ead162a9beec24089d574d1a2fb" title="View details: xubuntu-17.10.1-desktop-amd64">xubuntu 17 10 1 desk
top amd64</a> (<span style="color:red">Multi.</span>)   </strong></font><br/>
      Xubuntu is a community-developed operating system based on Ubuntu. It comes with Xfce, which is a stable, light and configurable desktop environment.<br/>
<hr/>
<table width="100%">
<tr><td>
<strong>Added On:</strong> 13/01/2018</td><td> </td></tr>
<tr> <td><strong>Size:</strong> 1.22 GB </td><td></td></tr>
<tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=5&amp;by=2">Seeds</a></strong> 126 </td><td></td></tr>
<tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=6&amp;by=2">Leechers</a></strong> 6 </td><td></td></tr>
<tr> <td width="90%"><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=7&amp;by=1">Completed</a></strong> 1557 </td><td align="right"><a href="mag
net:?xt=urn:btih:M3IGSO467V7K2FRKTPXMEQEJ2V2NDIX3"><img alt="Magnet Link" border="0" src="images/azureus.gif"/></a> <a href="index.php?page=downloadcheck&amp;id=66d0693b9efd7ead162a9be
ec24089d574d1a2fb"><img alt="torrent" border="0" src="images/download.gif"/></a>
</td></tr>
</table>
<hr/>
<table width="100%">
<tr>
<td>
---</td><td> <a href="index.php?page=userdetails&amp;id=9892">DEMONLORD</a></td><td>  N/A </td><td> N/A<br/></td>
<td align="center" class="lista" style="text-align: center;" width="20">---</td>
<td> <tag:torrents></tag:torrents></td><td><strong>
</strong></td></tr></table>
</td>
</tr>
<tr>
<td align="center" class="lista" width="125">
<center><a href="index.php?page=torrents&amp;category=2144"><img alt="Ubuntukylin" border="0" src="http://linuxtracker.org/style/Linuxtracker.New/images/categories/large/ubuntukylin.pn
g"/></a></center><p>
<a href="/torrentimg/noimage.jpg" rel="lightbox" title="view image">
<img src="thumbnail.php?size=150&amp;path=torrentimg/noimage.jpg"/></a><br/>
<a href="index.php?page=torrent-details&amp;id=48afd23dbe594df5bf5e88e3f74de7442b749cc0"><img src="/images/more_details_icon.png"/></a>
</p></td>
<td class="lista">
<font size="4"><strong><a href="index.php?page=torrent-details&amp;id=48afd23dbe594df5bf5e88e3f74de7442b749cc0" title="View details: ubuntukylin-17.10.1-desktop-i386">ubuntukylin 17 10
 1 desktop i386</a> (<span style="color:red">Multi.</span>)   </strong></font><br/>
      Ubuntu Kylin is an official Ubuntu subproject whose goal is to create a variant of Ubuntu that is more suitable for Chinese users using the Simplified Chinese writing system. The
 project provides a delicate, thoughtful and fully customised Chinese user experience out-of-the-box by providing a desktop user interface localised into Simplified Chinese and with so
ftware generally preferred by many Chinese users. Ubuntu Kylin was originally shipping with Ubuntu's Unity desktop, but starting with vers<br/>
<hr/>
<table width="100%">
<tr><td>
<strong>Added On:</strong> 13/01/2018</td><td> </td></tr>
<tr> <td><strong>Size:</strong> 1.59 GB </td><td></td></tr>
<tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=5&amp;by=2">Seeds</a></strong> 22 </td><td></td></tr>
<tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=6&amp;by=2">Leechers</a></strong> 0 </td><td></td></tr>
<tr> <td width="90%"><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=Ubuntu&amp;&amp;order=7&amp;by=1">Completed</a></strong> 32 </td><td align="right"><a href="magne
t:?xt=urn:btih:JCX5EPN6LFG7LP26RDR7OTPHIQVXJHGA"><img alt="Magnet Link" border="0" src="images/azureus.gif"/></a> <a href="index.php?page=downloadcheck&amp;id=48afd23dbe594df5bf5e88e3f
74de7442b749cc0"><img alt="torrent" border="0" src="images/download.gif"/></a>
</td></tr>
</table>
<hr/>
<table width="100%">
<tr>
<td>
---</td><td> <a href="index.php?page=userdetails&amp;id=9892">DEMONLORD</a></td><td>  N/A </td><td> N/A<br/></td>
<td align="center" class="lista" style="text-align: center;" width="20">---</td>
<td> <tag:torrents></tag:torrents></td><td><strong>
</strong></td></tr></table>
</td>
</tr>
<tr>
    """
        monkeypatch.setattr(linuxtracker.LinuxTracker, 'get', mock_get)
        return linuxtracker.LinuxTracker()
