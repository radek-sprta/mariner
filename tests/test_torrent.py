import pytest

from .context import mariner
from mariner import torrent


class TestTorrent:
    """
    Class to test Torrent methods.
    """

    @pytest.fixture
    def torrent(self):
        return torrent.Torrent(1, 'name', 'torrent', magnet_link='magnet',
                               description='desc')

    def test_id_is_int(self, torrent):
        """Id is integer."""
        assert isinstance(torrent.tid, int)

    def test_id_positive_number(self):
        with pytest.raises(ValueError):
            torrent.Torrent(-1, 'name', 'torrent')

    def test_name_is_string(self, torrent):
        """Name is a string."""
        assert isinstance(torrent.name, str)

    def test_torrent_url_is_string(self, torrent):
        """Torrent URL is a string."""
        assert isinstance(torrent.torrent_url, str)

    def test_magnet_link_is_string(self, torrent):
        """Magnet link is a string."""
        assert isinstance(torrent.magnet_link, str)

    def test_description_is_string(self, torrent):
        """Description is a string."""
        assert isinstance(torrent.description, str)

    def test_mods_is_string(self, torrent):
        """Description is a string."""
        assert isinstance(torrent.mods, str)

    def test_filename_is_string(self, torrent):
        """Description is a string."""
        assert isinstance(torrent.filename, str)
