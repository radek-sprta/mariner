import pytest

from mariner import torrent


class TestArchive:
    """
    Class to test Archive plugin.
    """
    @pytest.fixture(scope='module')
    def tracker(self, engine):
        return engine.plugins['archive']()

    @pytest.mark.vcr()
    def test_results(self, tracker, event_loop):
        # GIVEN a tracker and a title to search for
        # WHEN searching for it
        search = event_loop.run_until_complete(tracker.results('plan 9'))

        # THEN it should return a list of results
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) > 0
