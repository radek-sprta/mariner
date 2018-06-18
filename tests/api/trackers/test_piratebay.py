import pytest

from mariner import torrent


class TestPirateBay:
    """
    Class to test PirateBay plugin.
    """
    @pytest.fixture(scope='module')
    def tracker(self, engine):
        return engine.plugins['piratebay']()

    @pytest.mark.vcr()
    def test_results(self, tracker, event_loop):
        # GIVEN a tracker and a title to search for
        # WHEN searching for it
        search = event_loop.run_until_complete(tracker.results('ubuntu'))

        # THEN it should return a list of results
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) > 0

    def test_get_proxy(self, tracker, event_loop):
        proxy = event_loop.run_until_complete(tracker.get_proxy())
        assert isinstance(proxy, str)
        assert 'http' in proxy
