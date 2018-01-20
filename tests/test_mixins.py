import pytest

from mariner import torrent


class TestComparableMixin:

    @pytest.fixture
    def torrent1(self):
        return torrent.Torrent('name', 'tracker', seeds=10)

    @pytest.fixture
    def torrent2(self):
        return torrent.Torrent('name', 'tracker', seeds=20)

    def test_eq(self, torrent1, torrent2):
        """Equality comparison."""
        assert torrent1 == torrent1
        assert torrent2 == torrent2

    def test_ne(self, torrent1, torrent2):
        """Non equality comparison."""
        assert torrent1 != torrent2
        assert torrent2 != torrent1

    def test_lt(self, torrent1, torrent2):
        """Lesser then comparison."""
        assert torrent1 < torrent2
        assert not torrent2 < torrent1

    def test_gt(self, torrent1, torrent2):
        """Greater than comparison."""
        assert torrent2 > torrent1
        assert not torrent1 > torrent2

    def test_le(self, torrent1, torrent2):
        """Lesser equal comparison."""
        assert torrent1 <= torrent2
        assert torrent1 <= torrent1
        assert not torrent2 <= torrent1

    def test_ge(self, torrent1, torrent2):
        """Greater equal comparison."""
        assert torrent2 >= torrent1
        assert torrent2 >= torrent2
        assert not torrent1 >= torrent2
