import pathlib

import pytest
import vcr

from mariner import torrent


class TestKickAssTorrents:
    """
    Class to test KickAssTorrents plugin.
    """
    path = pathlib.Path(__file__)
    cassette = str(path.parent / 'cassettes' / (str(path.stem) + '.yaml'))

    @pytest.fixture(scope='module')
    def tracker(self, engine):
        return engine.plugins['kickasstorrents']()

    @vcr.use_cassette(cassette)
    def test_results(self, tracker, event_loop):
        # GIVEN a tracker and a title to search for
        # WHEN searching for it
        search = event_loop.run_until_complete(tracker.results('ubuntu'))

        # THEN it should return a list of results
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) > 0

    def test_parse_number(self, tracker):
        """Returns an integer out of number string."""
        assert tracker._parse_number('1,000,000') == 1000000
        assert tracker._parse_number('1 000 000') == 1000000
