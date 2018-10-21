import pytest

from mariner import torrent


class TestDistrowatch:
    """
    Class to test Distrowatch plugin.
    """
    @pytest.fixture(scope='module')
    def tracker(self, engine):
        return engine.plugins['distrowatch']()

    @pytest.mark.vcr()
    def test_results(self, tracker, event_loop):
        # GIVEN a tracker and a title to search for
        # WHEN searching for it
        search = event_loop.run_until_complete(tracker.results('ubuntu'))

        # THEN it should return a list of results
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) > 0

    @pytest.mark.vcr()
    def test_no_results(self, tracker, event_loop):
        # GIVEN a tracker and a nonexistant title
        # WHEN searching for it
        search = event_loop.run_until_complete(tracker.results('zxcvbnm'))

        # THEN it should return an empty list
        assert isinstance(search, list)
        assert len(search) == 0
