import pytest

from .context import mariner
from mariner import searchengine, torrent
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
        assert len(search) == 1

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
          <tbody><tr>
        <td class="lista" width="125">&nbsp;</td><td class="lista"></td></tr>
          <tr>
        <td class="lista" align="center" width="125">
<center><a href="index.php?page=torrents&amp;category=607"><img src="http://linuxtracker.org/style/Linuxtracker.New/images/categories/large/xubuntu.png" alt="Xubuntu" border="0"></a></center><p>
<a href="/torrentimg/noimage.jpg" title="view image" rel="lightbox">
      <img src="thumbnail.php?size=150&amp;path=torrentimg/noimage.jpg"></a><br>
            <a href="index.php?page=torrent-details&amp;id=456cc88a2b56ca09e22495ed6ec33e9d3d504e83"><img src="/images/more_details_icon.png"></a>
          </p></td>
        <td class="lista">
      <font size="4"><strong><a href="index.php?page=torrent-details&amp;id=456cc88a2b56ca09e22495ed6ec33e9d3d504e83" title="View details: xubuntu-17.10.1-desktop-i386">xubuntu 17 10 1 desktop i386</a> (<span style="color:red">Multi.</span>)   </strong></font><br>
            Xubuntu is a community-developed operating system based on Ubuntu. It comes with Xfce, which is a stable, light and configurable desktop environment.<br>
    <hr>
       <table width="100%">
       <tbody><tr><td>
          <strong>Added On:</strong> 13/01/2018</td><td> </td></tr>
    <tr> <td><strong>Size:</strong> 1.23 GB </td><td></td></tr>
    <tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=ubuntu&amp;&amp;order=5&amp;by=2">Seeds</a></strong> 53 </td><td></td></tr>
    <tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=ubuntu&amp;&amp;order=6&amp;by=2">Leechers</a></strong> 4 </td><td></td></tr>
    <tr> <td width="90%"><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=ubuntu&amp;&amp;order=7&amp;by=1">Completed</a></strong> 213 </td><td align="right"> <a href="magnet:?xt=urn:btih:IVWMRCRLK3FATYRESXWW5QZ6TU6VATUD"><img src="images/azureus.gif" alt="Magnet Link" border="0"></a><a href="index.php?page=downloadcheck&amp;id=456cc88a2b56ca09e22495ed6ec33e9d3d504e83"><img src="images/download.gif" alt="torrent" border="0"></a>
    </td></tr>
    </tbody></table>
    <hr>
    <table width="100%">
    <tbody><tr>
    <td>
    ---</td><td> <a href="index.php?page=userdetails&amp;id=9892">DEMONLORD</a></td><td>  N/A </td><td> N/A<br></td>

              <td class="lista" style="text-align: center;" align="center" width="20">---</td>



   <td>  <tag:torrents[].recommended></tag:torrents[].recommended></td><td><strong>

   </strong></td></tr></tbody></table>
   </td>

            </tr>
          <tr>
        <td class="lista" align="center" width="125">
<center><a href="index.php?page=torrents&amp;category=607"><img src="http://linuxtracker.org/style/Linuxtracker.New/images/categories/large/xubuntu.png" alt="Xubuntu" border="0"></a></center><p>
<a href="/torrentimg/noimage.jpg" title="view image" rel="lightbox">
      <img src="thumbnail.php?size=150&amp;path=torrentimg/noimage.jpg"></a><br>
            <a href="index.php?page=torrent-details&amp;id=66d0693b9efd7ead162a9beec24089d574d1a2fb"><img src="/images/more_details_icon.png"></a>
          </p></td>
        <td class="lista">
      <font size="4"><strong><a href="index.php?page=torrent-details&amp;id=66d0693b9efd7ead162a9beec24089d574d1a2fb" title="View details: xubuntu-17.10.1-desktop-amd64">xubuntu 17 10 1 desktop amd64</a> (<span style="color:red">Multi.</span>)   </strong></font><br>
            Xubuntu is a community-developed operating system based on Ubuntu. It comes with Xfce, which is a stable, light and configurable desktop environment.<br>
    <hr>
       <table width="100%">
       <tbody><tr><td>
          <strong>Added On:</strong> 13/01/2018</td><td> </td></tr>
    <tr> <td><strong>Size:</strong> 1.22 GB </td><td></td></tr>
    <tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=ubuntu&amp;&amp;order=5&amp;by=2">Seeds</a></strong> 129 </td><td></td></tr>
    <tr> <td><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=ubuntu&amp;&amp;order=6&amp;by=2">Leechers</a></strong> 5 </td><td></td></tr>
    <tr> <td width="90%"><strong><a href="/index.php?page=torrents&amp;active=1&amp;search=ubuntu&amp;&amp;order=7&amp;by=1">Completed</a></strong> 731 </td><td align="right"><a href="magnet:?xt=urn:btih:M3IGSO467V7K2FRKTPXMEQEJ2V2NDIX3"><img src="images/azureus.gif" alt="Magnet Link" border="0"></a> <a href="index.php?page=downloadcheck&amp;id=66d0693b9efd7ead162a9beec24089d574d1a2fb"><img src="images/download.gif" alt="torrent" border="0"></a>
    </td></tr>
    </tbody></table>
    <hr>
    <table width="100%">
    <tbody><tr>
    <td>
    ---</td><td> <a href="index.php?page=userdetails&amp;id=9892">DEMONLORD</a></td><td>  N/A </td><td> N/A<br></td>
</table>
    """
        monkeypatch.setattr(linuxtracker.LinuxTracker, 'get', mock_get)
        return linuxtracker.LinuxTracker()
