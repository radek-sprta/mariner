import pytest

from mariner import torrent


class TestTokyoTosho:
    """
    Class to test TokyoTosho plugin.
    """

    @pytest.fixture(scope="module")
    def tracker(self, engine):
        return engine.plugins["tokyotosho"]()

    @pytest.mark.vcr()
    def test_results(self, tracker, event_loop):
        # GIVEN a tracker and a title to search for
        # WHEN searching for it
        search = event_loop.run_until_complete(tracker.results("ubuntu"))

        # THEN it should return a list of results
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) > 0

        # AND the results should all have a title
        for result in search:
            assert result.name != None

    @pytest.mark.vcr()
    def test_no_results(self, tracker, event_loop):
        # GIVEN a tracker
        # WHEN searching for nonexistant title
        search = event_loop.run_until_complete(tracker.results("zxcvbnm"))

        # THEN it should return an empty list
        search = list(search)
        assert search == []
        assert len(search) == 0
