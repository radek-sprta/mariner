import pytest

from .context import mariner
from mariner import exceptions, searchengine, torrent


@pytest.fixture(scope='module')
def engine():
    return searchengine.SearchEngine()


class TestSearchEngine:
    """Test SearchEngine methods."""

    def test_initialize_plugins(self, engine):
        assert engine.plugins
        assert 'linuxtracker' in engine.plugins.keys()
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
        trackers = ['linuxtracker', 'distrowatch', 'kickasstorrents']
        results = engine._cached_search(title, trackers, timeout=10)
        for result in results:
            assert isinstance(result, torrent.Torrent)
            assert title.lower() in result.name.lower()
            assert result.tracker.lower() in trackers

    @pytest.mark.parametrize('limit', [5, 10, 15])
    def test_search(self, engine, limit):
        """Search for torrent on given trackers."""
        title = 'Ubuntu'
        trackers = ['linuxtracker', 'distrowatch', 'kickasstorrents']
        results = engine.search(title, trackers, limit=limit)
        assert len(results) == limit
        for __, result in results:
            assert isinstance(result, torrent.Torrent)
            assert title.lower() in result.name.lower()
            assert result.tracker.lower() in trackers

    def test_search_no_title(self, engine):
        """Search for torrent on given trackers."""
        title = ''
        trackers = ['linuxtracker', 'distrowatch', 'kickasstorrents']
        with pytest.raises(exceptions.InputError):
            engine.search(title, trackers)

    def test_search_no_tracker(self, engine):
        """Search for torrent on given trackers."""
        title = 'Ubuntu'
        trackers = []
        with pytest.raises(exceptions.InputError):
            engine.search(title, trackers)

    def test_search_no_result(self, engine):
        """Search for torrent on given trackers."""
        title = 'qwertyzxcvb'
        trackers = ['linuxtracker', 'distrowatch', 'kickasstorrents']
        with pytest.raises(exceptions.NoResultException):
            engine.search(title, trackers)

    def test_search_newest(self, engine):
        """Search for torrent on given trackers and sort them by newest."""
        title = 'Ubuntu'
        trackers = ['linuxtracker', 'distrowatch', 'kickasstorrents']
        results = engine.search(title, trackers, sort_by_newest=True)
        for i, result in results[:-1]:
            assert isinstance(result, torrent.Torrent)
            assert title.lower() in result.name.lower()
            assert result.tracker.lower() in trackers
            assert result.date >= results[i + 1][1].date

    def test_search_limit_zero(self, engine):
        """Search throws InputError when limit is zero."""
        title = 'Ubuntu'
        trackers = ['linuxtracker', 'distrowatch']
        with pytest.raises(exceptions.InputError):
            engine.search(title, trackers, limit=0)

    @pytest.mark.parametrize('tid', [1, 2, 3])
    def test_result(self, engine, tid):
        """Get torrent with given ID."""
        result = engine.result(tid)
        assert isinstance(result, torrent.Torrent)

    @pytest.mark.parametrize('tid', [-1, -9999, 1000000])
    def test_result_nonexistant(self, engine, tid):
        """Asking for nonexistant torrent ID throws NoResultException."""
        with pytest.raises(exceptions.NoResultException):
            engine.result(tid)

    def test_save_results(self, engine):
        """Save search results into cache."""
        tid = 10000
        torrent = 'test'
        engine.save_results([(tid, torrent)])
        assert engine.result(tid) == torrent
