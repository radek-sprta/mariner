import pytest

from mariner import torrent
from mariner.trackers import etree


class TestEtree:
    """
    Class to test Etree plugin.
    """

    def test_results(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('wilco'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 3

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return Etree instance."""
        async def mock_get(*args, **kwargs):
            return """
            <table></table><table></table><table></table><table></table><table></table>
<table border="0" bgcolor="#CCCCCC" width="100%" cellpadding="3">
<tbody>
<tr></tr>
<tr bgcolor="#ffffff" align="right">
 <td align="left">
  <a href="/index.php?searchzz=wilco&amp;cat=184">Wilco</a>
 </td>
 <td align="left">
  <a class="details_link" href="details.php?id=598098"><b>Wilco1998-06-28 Fleadh Festival San Jose'  CA ( SBD-AUD Matrix )</b></a>
        <!--        &nbsp;<span class="red">*NEW*</span> -->
     </td>
 <td>
  <a href="download.php/598098/Wilco1998-06-28%20Fleadh%20Festival%20San%20Jose%27%20%20CA%20%28%20SBD-AUD%20Matrix%20%29.torrent"><img src="/pic/disk.gif" alt="[download]"></a>
 </td>
 <td>
  <a href="details.php?id=598098&amp;filelist=1#filelist">16</a>
 </td>
 <td>
  <a href="details.php?id=598098#startcomments">0</a>
 </td>
 <td>02/17 11:46</td>
 <td>277.17 MB</td>
 <td>76 times</td>
 <td><a href="details.php?id=598098&amp;dllist=1#seeders">3</a></td>
 <td><a class="red" href="details.php?id=598098&amp;dllist=1#leechers">0</a></td>
        <td align="left"><a href="http://db.etree.org/KerouacAW">KerouacAW</a></td>
</tr>
<tr bgcolor="#ffffff" align="right">
 <td align="left">
  <a href="/index.php?searchzz=wilco&amp;cat=184">Wilco</a>
 </td>
 <td align="left">
  <a class="details_link" href="details.php?id=597956"><b>Wilco 1995-08-24 Mann Music Center-Philadelphia,PA HORDE Tour (SBD)</b></a>
        <!--        &nbsp;<span class="red">*NEW*</span> -->
     </td>
 <td>
  <a href="download.php/597956/Wilco%201995-08-24%20Mann%20Music%20Center-Philadelphia%2CPA%20HORDE%20Tour%20%28SBD%29.torrent"><img src="/pic/disk.gif" alt="[download]"></a>
 </td>
 <td>
  <a href="details.php?id=597956&amp;filelist=1#filelist">15</a>
 </td>
 <td>
  <a href="details.php?id=597956#startcomments">2</a>
 </td>
 <td>02/10 23:51</td>
 <td>206.23 MB</td>
 <td>92 times</td>
 <td><a href="details.php?id=597956&amp;dllist=1#seeders">2</a></td>
 <td><a class="red" href="details.php?id=597956&amp;dllist=1#leechers">0</a></td>
        <td align="left"><a href="http://db.etree.org/KerouacAW">KerouacAW</a></td>
</tr>
<tr bgcolor="#ffffff" align="right">
 <td align="left">
  <a href="/index.php?searchzz=wilco&amp;cat=184">Wilco</a>
 </td>
 <td align="left">
  <a class="details_link" href="details.php?id=597917"><b>Wilco 2002-05-26_Melweg - Amsterdam,NL  (Matrix)</b></a>
        <!--        &nbsp;<span class="red">*NEW*</span> -->
     </td>
 <td>
  <a href="download.php/597917/Wilco%202002-05-26_Melweg%20-%20Amsterdam%2CNL%20%20%28Matrix%29.torrent"><img src="/pic/disk.gif" alt="[download]"></a>
 </td>
 <td>
  <a href="details.php?id=597917&amp;filelist=1#filelist">27</a>
 </td>
 <td>
  <a href="details.php?id=597917#startcomments">4</a>
 </td>
 <td>02/09 13:12</td>
 <td>672.24 MB</td>
 <td>111 times</td>
 <td><a href="details.php?id=597917&amp;dllist=1#seeders">2</a></td>
 <td><a class="red" href="details.php?id=597917&amp;dllist=1#leechers">0</a></td>
        <td align="left"><a href="http://db.etree.org/KerouacAW">KerouacAW</a></td>
</tr>
</tbody></table>
            """
        monkeypatch.setattr(etree.Etree, 'get', mock_get)
        return etree.Etree()
