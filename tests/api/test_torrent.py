import datetime

import pytest

from mariner import torrent


class TestTorrent:
    """
    Class to test Torrent methods.
    """

    @pytest.fixture(scope='module')
    def torrents(self):
        return [torrent.Torrent('name', 'tracker', date='today', seeds=1, leeches=10),
                torrent.Torrent('name', 'tracker', date='2018-01-01', seeds=2, leeches=10)]

    @pytest.mark.smoke
    def test_defaults(self):
        default = torrent.Torrent('name', 'tracker')
        expected = torrent.Torrent('name', 'tracker', torrent=None,
                                   magnet=None, size='Unknown', seeds=-1, leeches=None, date=None)
        assert default == expected

    @pytest.mark.smoke
    def test_member_access(self, torrents):
        torrent = torrents[0]
        assert torrent.name == 'name'
        assert torrent.tracker == 'tracker'
        assert torrent.torrent == None
        assert torrent.magnet == None
        assert torrent.size == 'Unknown'
        assert torrent.seeds == 1
        assert torrent.leeches == 10
        assert torrent.date == datetime.date.today()
        assert torrent.filename == 'name.torrent'

    @pytest.mark.smoke
    def test_comparison(self, torrents):
        assert torrents[0] < torrents[1]
        assert torrents[0] <= torrents[1]
        assert torrents[0] <= torrents[0]
        assert torrents[1] > torrents[0]
        assert torrents[1] >= torrents[0]
        assert torrents[0] >= torrents[0]
        assert torrents[1] != torrents[0]
        assert torrents[0] == torrents[0]

    @pytest.mark.smoke
    def test_colored(self, torrents):
        for torrent in torrents:
            assert '33m' in torrent.colored().name
            assert '32m' in torrent.colored().seeds
            assert '31m' in torrent.colored().leeches

    def test_representation(self, torrents):
        date = datetime.date.today()
        expected = 'Torrent(name, tracker, None, None, Unknown, 1, 10, {date})'.format(
            date=date)
        assert str(torrents[0]) == expected
