import pytest

from .context import mariner
from mariner import searchengine, torrent


@pytest.fixture(scope='module')
def engine():
    return searchengine.SearchEngine()


class TestSearchEngine:
    """Test SearchEngine methods."""

    def test_initialize_plugins(self, engine):
        assert engine.plugins
        assert 'piratebay' in engine.plugins.keys()
        assert 'distrowatch' in engine.plugins.keys()
        assert 'tokyotosho' in engine.plugins.keys()

    def test_flatten(self, engine):
        """Flatten nested list."""
        nested_list = [[1, 2, 3], [4], [5, 6]]
        flattened_list = [1, 2, 3, 4, 5, 6]
        assert engine._flatten(nested_list) == flattened_list

    def test_cached_search(self, engine):
        """Search for torrent on given trackers."""
        title = 'Ubuntu'
        trackers = ['piratebay', 'distrowatch']
        results = engine._cached_search(title, trackers)
        for result in results:
            assert isinstance(result, torrent.Torrent)
            assert title.lower() in result.name.lower()
            assert result.tracker.lower() in trackers

    @pytest.mark.parametrize('limit', [10, 20, 30])
    def test_search(self, engine, limit):
        """Search for torrent on given trackers."""
        title = 'Ubuntu'
        trackers = ['piratebay', 'distrowatch']
        results = engine.search(title, trackers, limit=limit)
        assert len(results) == limit
        for __, result in results:
            assert isinstance(result, torrent.Torrent)
            assert title.lower() in result.name.lower()
            assert result.tracker.lower() in trackers

    def test_search_limit_zero(self, engine):
        """Search throws ValueError when limit is zero."""
        title = 'Ubuntu'
        trackers = ['piratebay', 'distrowatch']
        with pytest.raises(ValueError):
            engine.search(title, trackers, limit=0)

    @pytest.mark.parametrize('tid', [1, 2, 3])
    def test_result(self, engine, tid):
        """Get torrent with given ID."""
        result = engine.result(tid)
        assert isinstance(result, torrent.Torrent)

    @pytest.mark.parametrize('tid', [-1, -9999, 1000000])
    def test_result_nonexistant(self, engine, tid):
        """Asking for nonexistant torrent ID throws NoResultException."""
        with pytest.raises(searchengine.NoResultException):
            engine.result(tid)

    def test_save_results(self, engine):
        """Save search results into cache."""
        tid = 10000
        torrent = 'test'
        engine.save_results([(tid, torrent)])
        assert engine.result(tid) == torrent


class TestExceptions:
    """Test exception existance."""

    def test_base_error(self):
        """Error exists."""
        exception = searchengine.Error()
        assert exception
        assert Exception in exception.__class__.__bases__

    def test_no_result_exception(self):
        """NoResultException exists."""
        exception = searchengine.NoResultException()
        assert exception
        assert searchengine.Error in exception.__class__.__bases__
