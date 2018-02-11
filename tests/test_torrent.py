import datetime

import pytest

from .context import mariner
from mariner import torrent


class TestTorrent:
    """
    Class to test Torrent methods.
    """

    @pytest.fixture
    def torrent(self):
        return torrent.Torrent('name', 'tracker', date='yesterday', magnet='magnet', torrent='tracker')

    def test_name_is_string(self, torrent):
        """Name is a string."""
        assert isinstance(torrent.name, str)

    def test_torrent_is_string(self, torrent):
        """Torrent URL is a string."""
        assert isinstance(torrent.torrent, str)

    def test_magnet_is_string(self, torrent):
        """Magnet link is a string."""
        assert isinstance(torrent.magnet, str)

    def test_tracker_is_string(self, torrent):
        """Tracker is a string."""
        assert isinstance(torrent.tracker, str)

    def test_filename_is_string(self, torrent):
        """Filename is a string."""
        assert isinstance(torrent.filename, str)

    def test_cmpkey_is_int(self, torrent):
        """_cmpkey is an integer."""
        assert isinstance(torrent._cmpkey, int)

    def test_date_is_mayadt(self, torrent):
        """Filename is a string."""
        assert isinstance(torrent.date, datetime.date)
