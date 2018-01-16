import pytest

from .context import mariner
from mariner import torrent


class TestTorrent:
    """
    Class to test Torrent methods.
    """

    @pytest.fixture
    def torrent(self):
        return torrent.Torrent('name', 'tacker', magnet_link='magnet', torrent_url='tracker')

    def test_name_is_string(self, torrent):
        """Name is a string."""
        assert isinstance(torrent.name, str)

    def test_torrent_url_is_string(self, torrent):
        """Torrent URL is a string."""
        assert isinstance(torrent.torrent_url, str)

    def test_magnet_link_is_string(self, torrent):
        """Magnet link is a string."""
        assert isinstance(torrent.magnet_link, str)

    def test_tracker_is_string(self, torrent):
        """Tracker is a string."""
        assert isinstance(torrent.tracker, str)

    def test_filename_is_string(self, torrent):
        """Filename is a string."""
        assert isinstance(torrent.filename, str)
