import pytest


class TestSearch:
    @pytest.fixture(scope="class")
    def expected(self):
        return [
            '"\x1b[35mID\x1b[0m","\x1b[35mName\x1b[0m","\x1b[35mTracker\x1b[0m","\x1b[35mSeeds\x1b[0m","\x1b[35mSize\x1b[0m","\x1b[35mUploaded\x1b[0m","\x1b[35mAvailable as\x1b[0m"\n',
            '0,"\x1b[33mubuntustudio-12.04-dvd-amd64.iso\x1b[0m","TokyoTosho","\x1b[32m0\x1b[0m","1.92GB","2012-07-14","Magnet link, Torrent"\n',
            '1,"\x1b[33mubuntu-13.04-desktop-i386.iso\x1b[0m","TokyoTosho","\x1b[32m0\x1b[0m","794MB","2013-04-25","Magnet link, Torrent"\n',
            '2,"\x1b[33mubuntu-13.04-server-amd64.iso\x1b[0m","TokyoTosho","\x1b[32m0\x1b[0m","701MB","2013-04-25","Magnet link, Torrent"\n',
        ]

    def test_search(self, run, expected):
        # GIVEN a search term
        # WHEN searching for it
        result = run("search", "-f", "csv", "-t", "tokyotosho", "ubuntu")[0]

        # THEN a table of results should be returned
        assert result == "".join(expected)

    def test_search_newest(self, run):
        # GIVEN a search term
        # WHEN searching for it with the --newest flag
        result = run("search", "-f", "csv", "-t", "tokyotosho", "ubuntu", "--newest")[0]

        # THEN the results should be ordered in most recent first order
        expected = (
            '"\x1b[35mID\x1b[0m","\x1b[35mName\x1b[0m","\x1b[35mTracker\x1b[0m","\x1b[35mSeeds\x1b[0m","\x1b[35mSize\x1b[0m","\x1b[35mUploaded\x1b[0m","\x1b[35mAvailable as\x1b[0m"\n'
            '0,"\x1b[33mubuntu-13.04-desktop-i386.iso\x1b[0m","TokyoTosho","\x1b[32m0\x1b[0m","794MB","2013-04-25","Magnet link, Torrent"\n'
            '1,"\x1b[33mubuntu-13.04-server-amd64.iso\x1b[0m","TokyoTosho","\x1b[32m0\x1b[0m","701MB","2013-04-25","Magnet link, Torrent"\n'
            '2,"\x1b[33mubuntustudio-12.04-dvd-amd64.iso\x1b[0m","TokyoTosho","\x1b[32m0\x1b[0m","1.92GB","2012-07-14","Magnet link, Torrent"\n'
        )
        assert result == expected

    @pytest.mark.parametrize("limit", [1, 2, 3])
    def test_search_limit(self, run, limit, expected):
        # GIVEN a search term
        # WHEN searching for it with --limit flag
        result = run("search", "-f", "csv", "-t", "tokyotosho", "ubuntu", "--limit", str(limit))[0]

        # THEN the number of results should be equal or lower than the limit
        assert result <= "".join(expected[: limit + 1])

    def test_search_legal(self, run):
        # GIVEN a search term
        # WHEN searching for it with --legal flag
        result = run("search", "-f", "csv", "plan 9 from outer space", "--legal", "--limit", "3")[0]

        # THEN the results should only come from legal trackers
        expected = [
            '"\x1b[35mID\x1b[0m","\x1b[35mName\x1b[0m","\x1b[35mTracker\x1b[0m","\x1b[35mSeeds\x1b[0m","\x1b[35mSize\x1b[0m","\x1b[35mUploaded\x1b[0m","\x1b[35mAvailable as\x1b[0m"\n',
            '0,"\x1b[33mPlan 9 from Outer Space\x1b[0m","Archive","\x1b[32m-1\x1b[0m","Unknown","0001-01-01","Torrent"\n',
            '1,"\x1b[33mPlan 9 from Outer Space (1958)\x1b[0m","Archive","\x1b[32m-1\x1b[0m","Unknown","0001-01-01","Torrent"\n',
            '2,"\x1b[33mPlan 9 from Outer Space\x1b[0m","Archive","\x1b[32m-1\x1b[0m","Unknown","0001-01-01","Torrent"\n',
        ]
        for line in expected:
            assert line in result
