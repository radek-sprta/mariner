import pytest

from mariner import torrent
from mariner.trackers import nyaa


class TestNyaa:
    """
    Class to test Nyaa plugin.
    """

    def test_results(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('Ubuntu'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 1

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return Nyaa instance."""
        async def mock_get(*args, **kwargs):
            return """
            <tr class="default">
            <td style="padding:0 4px;">
            <a href="/?c=6_1" title="Software - Applications">
                <img src="/static/img/icons/nyaa/6_1.png" alt="Software - Applications">
            </a>
            </td>
            <td colspan="2">
                <a href="/view/96659" title="Koha Live CD Release 3 (3.0.4 Ubuntu 9.10 Desktop x86)">Koha Live CD Release 3 (3.0.4 Ubuntu 9.10 Desktop x86)</a>
            </td>
            <td class="text-center" style="white-space: nowrap;"><a href="/download/96659.torrent"><i class="fa fa-fw fa-download"></i></a><a href="magnet:?xt=urn:btih:IUAI4SGIQAFX25SDGN5S44FGGTSMNH3K&amp;dn=Koha+Live+CD+Release+3+%283.0.4+Ubuntu+9.10+Desktop+x86%29&amp;tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&amp;tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&amp;tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce"><i class="fa fa-fw fa-magnet"></i></a>
            </td>
            <td class="text-center">624.0 MiB</td>
            <td class="text-center" data-timestamp="1257231780" title="8 years 4 months 1 week 5 days 22 hours 34 minutes 50 seconds ago">2009-11-03 08:03</td>

            <td class="text-center" style="color: green;">0</td>
            <td class="text-center" style="color: red;">0</td>
            <td class="text-center">0</td>
            </tr> """
        monkeypatch.setattr(nyaa.Nyaa, 'get', mock_get)
        return nyaa.Nyaa()
