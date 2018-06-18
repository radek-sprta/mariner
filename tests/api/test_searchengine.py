import pytest

from mariner import exceptions, torrent


class TestSearchEngine:

    @pytest.fixture(scope='class')
    def trackers(self, engine):
        trackers = engine.plugins.keys()
        return [t for t in trackers if t not in ['kat', 'kickasstorrents']]

    @pytest.mark.smoke
    def test_initialize_plugins(self, engine):
        # GIVEN that plugins are initialized
        assert engine.plugins

        # WHEN adding checking plugins from the plugins directory
        plugins = [str(p.stem) for p in engine.plugin_directory.glob('*.py')]

        # THEN they should be loaded
        for plugin in plugins:
            if plugin == '__init__':
                continue
            assert plugin in engine.plugins.keys()

    @pytest.mark.parametrize('lists',
                             [{'nested': [[1, 2, 3], [4], [5, 6]], 'flat': [1, 2, 3, 4, 5, 6]},
                              {'nested': [[]], 'flat': []},
                                 {'nested': [[1], [2], [3], [4], [5], [6]], 'flat': [1, 2, 3, 4, 5, 6]}])
    def test_flatten(self, engine, lists):
        # GIVEN a nested list
        # WHEN using _flatten
        # THEN it should be flatteneted
        assert engine._flatten(lists['nested']) == lists['flat']

    @pytest.mark.smoke
    @pytest.mark.parametrize('limit', [5, 10, 15])
    @pytest.mark.vcr()
    def test_search(self, engine, limit, trackers, title):
        # GIVEN a title to search for and a list of trackers
        # WHEN searching for it on various trackers
        results = engine.search(title, trackers, limit=limit)

        # THEN a number of results equal to the limit should be returned
        assert len(results) == limit
        for i, result in results[:-1]:
            assert isinstance(result, torrent.Torrent)
            assert title.lower() in result.name.lower()
            assert result.tracker.lower() in trackers
            assert result.seeds >= results[i + 1][1].seeds

    def test_search_no_title(self, engine, trackers):
        # GIVEN no title
        title = ''

        # WHEN searching for it on a list of trackers
        # THEN it should raise exception
        with pytest.raises(exceptions.InputError):
            engine.search(title, trackers)

    def test_search_no_tracker(self, engine, title):
        # GIVEN a title
        # WHEN searching for it on no trackers
        trackers = []

        # THEN an exception should be raised
        with pytest.raises(exceptions.InputError):
            engine.search(title, trackers)

    @pytest.mark.vcr()
    def test_search_no_result(self, engine, trackers):
        # GIVEN a title that will yield no results and list of trackers
        title = 'qwertyzxcvb'

        # WHEN searching for results
        # THEN an exception should be raised
        with pytest.raises(exceptions.NoResultException):
            engine.search(title, trackers)

    @pytest.mark.vcr()
    def test_search_newest(self, engine, trackers, title):
        # GIVEN a title to search for on a list of trackers
        # WHEN search for results sorted by date
        results = engine.search(title, trackers, sort_by_newest=True)

        # THEN the list of results should be ordered by date
        for i, result in results[:-1]:
            assert isinstance(result, torrent.Torrent)
            assert result.tracker.lower() in trackers
            assert result.date >= results[i + 1][1].date

    def test_search_limit_zero(self, engine, trackers, title):
        # GIVEN a title to search for and a list of trackers
        # WHEN search for results with limit set to zero
        # THEN an exception should be raised
        with pytest.raises(exceptions.InputError):
            engine.search(title, trackers, limit=0)

    @pytest.mark.smoke
    @pytest.mark.parametrize('tid', [1, 2, 3])
    def test_result(self, engine, tid):
        # GIVEN an id
        # WHEN searching the results for the that id
        result = engine.result(tid)

        # THEN a Torrent with should be returned
        assert isinstance(result, torrent.Torrent)

    @pytest.mark.smoke
    @pytest.mark.parametrize('tid', [-1, -9999, 1000000])
    def test_result_nonexistant(self, engine, tid):
        # GIVEN a nonexistant id
        # WHEN searching the results for that id
        # THEN an exception should be raised
        with pytest.raises(exceptions.NoResultException):
            engine.result(tid)

    @pytest.mark.smoke
    @pytest.mark.parametrize('tid', [100, 1000, 10000])
    def test_save_results(self, engine, tid):
        # GIVEN a torrent with id
        torrent = 'test'

        # WHEN saving the torrent
        engine.save_results([(tid, torrent)])

        # THEN it should be in the database
        assert engine.results.get(tid) == torrent

    @pytest.mark.parametrize('timeout', [0, -1, -100])
    def test_negative_timeout(self, engine, timeout):
        # GIVEN a search engine
        # WHEN trying to set a negative timeout
        # THEN an exception should be raised
        with pytest.raises(exceptions.ConfigurationError):
            engine.timeout = timeout

    def test_nonexistant_tracker(self, title, engine):
        # GIVEN a search engine
        # WHEN trying to search on a nonexistant tracker
        trackers = ['nonsense', 'invalid']

        # THEN an exception should be raised
        with pytest.raises(exceptions.ConfigurationError):
            engine.search(title, trackers)
