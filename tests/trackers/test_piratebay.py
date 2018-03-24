import pytest

from mariner import torrent
from mariner.trackers import piratebay


class TestPirateBay:
    """
    Class to test PirateBay plugin.
    """

    def test_result(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('Ubuntu'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3

    def test_get_proxy(self, engine, event_loop):
        proxy = event_loop.run_until_complete(engine.get_proxy())
        assert isinstance(proxy, str)
        assert 'http' in proxy

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return PirateBay instance."""
        async def mock_get(*args, **kwargs):
            return """
<html>
 <body>
  <table id="searchResult">
  <thead>
    <tr>Header</tr>
  </thead>
  <tr>
   <td class="vertTh">
    <center>
     <a href="/browse/600" title="More from this category">
      Other
     </a>
     <br/>
     (
     <a href="/browse/699" title="More from this category">
      Other
     </a>
     )
    </center>
   </td>
   <td>
    <div class="detName">
     <a class="detLink" href="/torrent/14431396/Udemy_-_Ubuntu_Linux_-_Go_from_Beginner_to_Power_User" title="Details for Udemy - Ubuntu Linux - Go from Beginner to Power User">
      Udemy - Ubuntu Linux - Go from Beginner to Power User
     </a>
    </div>
    <a href="magnet:?xt=urn:btih:5f90af9933d5613520487fafbaae79f91d1711ed&amp;dn=Udemy+-+Ubuntu+Linux+-+Go+from+Beginner+to+Power+User&amp;tr=udp%3A%2F%2Ftracker.leechers-paradise.org%
3A6969&amp;tr=udp%3A%2F%2Fzer0day.ch%3A1337&amp;tr=udp%3A%2F%2Fopen.demonii.com%3A1337&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&amp;tr=udp%3A%2F%2Fexodus.desync.com%3A6969" ti
tle="Download this torrent using magnet">
     <img alt="Magnet link" src="//thepiratebay.org/static/img/icon-magnet.gif"/>
    </a>
    <img alt="This torrent has 1 comments." src="//thepiratebay.org/static/img/icon_comment.gif" title="This torrent has 1 comments."/>
    <a href="/user/Horisarte">
     <img alt="VIP" border="0" src="//thepiratebay.org/static/img/vip.gif" style="width:11px;" title="VIP"/>
    </a>
    <font class="detDesc">
     Uploaded 04-25 2016, Size 2.43 GiB, ULed by
     <a class="detDesc" href="/user/Horisarte/" title="Browse Horisarte">
      Horisarte
     </a>
    </font>
   </td>
   <td align="right">
    18
   </td>
   <td align="right">
    6
   </td>
  </tr>
  <tr class="alt">
   <td class="vertTh">
    <center>
     <a href="/browse/200" title="More from this category">
      Video
     </a>
    <br/>
     (
     <a href="/browse/299" title="More from this category">
      Other
     </a>
     )
    </center>
   </td>
   <td>
    <div class="detName">
     <a class="detLink" href="/torrent/9681585/Infiniteskills_-_Learning_Ubuntu_Linux" title="Details for Infiniteskills - Learning Ubuntu Linux">
      Infiniteskills - Learning Ubuntu Linux
     </a>
    </div>
    <a href="magnet:?xt=urn:btih:7c7dca2ac0d7d5c3526fb21fd52b260e6967719e&amp;dn=Infiniteskills+-+Learning+Ubuntu+Linux&amp;tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&amp;tr=u
dp%3A%2F%2Fzer0day.ch%3A1337&amp;tr=udp%3A%2F%2Fopen.demonii.com%3A1337&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&amp;tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download t
his torrent using magnet">
     <img alt="Magnet link" src="//thepiratebay.org/static/img/icon-magnet.gif"/>
    </a>
    <img alt="This torrent has 9 comments." src="//thepiratebay.org/static/img/icon_comment.gif" title="This torrent has 9 comments."/>
    <a href="/user/NepsterJay">
     <img alt="VIP" border="0" src="//thepiratebay.org/static/img/vip.gif" style="width:11px;" title="VIP"/>
    </a>
    <font class="detDesc">
     Uploaded 03-01 2014, Size 810.69 MiB, ULed by
     <a class="detDesc" href="/user/NepsterJay/" title="Browse NepsterJay">
      NepsterJay
     </a>
    </font>
   </td>
   <td align="right">
    14
   </td>
   <td align="right">
    1
   </td>
  </tr>
  <tr>
   <td class="vertTh">
    <center>
     <a href="/browse/300" title="More from this category">
      Applications
     </a>
     <br/>
     (
     <a href="/browse/303" title="More from this category">
      UNIX
     </a>
     )
    </center>
   </td>
   <td>
    <div class="detName">
     <a class="detLink" href="/torrent/11887232/Ubuntu_15.04_Desktop_i386__[Iso_-_MultiLang]_[TNTVillage]" title="Details for Ubuntu 15.04 Desktop i386, [Iso - MultiLang] [TNTVillage]" >
      Ubuntu 15.04 Desktop i386, [Iso - MultiLang] [TNTVillage]
     </a>
    </div>
    <a href="magnet:?xt=urn:btih:4896fde14efbc0f66a274d2a69104fbb57fbd2cb&amp;dn=Ubuntu+15.04+Desktop+i386%2C+%5BIso+-+MultiLang%5D+%5BTNTVillage%5D&amp;tr=udp%3A%2F%2Ftracker.leechers
-paradise.org%3A6969&amp;tr=udp%3A%2F%2Fzer0day.ch%3A1337&amp;tr=udp%3A%2F%2Fopen.demonii.com%3A1337&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&amp;tr=udp%3A%2F%2Fexodus.desync.
com%3A6969" title="Download this torrent using magnet">
     <img alt="Magnet link" src="//thepiratebay.org/static/img/icon-magnet.gif"/>
    </a>
    <a href="/user/mykons">
     <img alt="Trusted" border="0" src="//thepiratebay.org/static/img/trusted.png" style="width:11px;" title="Trusted"/>
    </a>
    <img src="//thepiratebay.org/static/img/11x11p.png"/>
    <font class="detDesc">
     Uploaded 05-05 2015, Size 1.11 GiB, ULed by
     <a class="detDesc" href="/user/mykons/" title="Browse mykons">
      mykons
     </a>
    </font>
   </td>
   <td align="right">
    10
   </td>
   <td align="right">
    3
   </td>
  </tr>
  </table>
 </body>
</html>
                """
        monkeypatch.setattr(piratebay.PirateBay, 'get', mock_get)
        return piratebay.PirateBay()
