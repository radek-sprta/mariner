import pytest


class TestSearch:
    @pytest.fixture(scope="class")
    def expected(self):
        return [
            '"ID","Name","Tracker","Seeds","Size","Uploaded","Available as"\n',
            '0,"ubuntustudio-12.04-dvd-amd64.iso","TokyoTosho","0","1.92GB","2012-07-14","Magnet link, Torrent"\n',
            '1,"ubuntu-13.04-desktop-i386.iso","TokyoTosho","0","794MB","2013-04-25","Magnet link, Torrent"\n',
            '2,"ubuntu-13.04-server-amd64.iso","TokyoTosho","0","701MB","2013-04-25","Magnet link, Torrent"\n',
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
            '"ID","Name","Tracker","Seeds","Size","Uploaded","Available as"\n'
            '0,"ubuntu-13.04-desktop-i386.iso","TokyoTosho","0","794MB","2013-04-25","Magnet link, Torrent"\n'
            '1,"ubuntu-13.04-server-amd64.iso","TokyoTosho","0","701MB","2013-04-25","Magnet link, Torrent"\n'
            '2,"ubuntustudio-12.04-dvd-amd64.iso","TokyoTosho","0","1.92GB","2012-07-14","Magnet link, Torrent"\n'
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
        result = run("search", "-f", "csv", "one body too many", "--legal", "--limit", "3")[0]

        # THEN the results should only come from legal trackers
        expected = [
            '"ID","Name","Tracker","Seeds","Size","Uploaded","Available as"\n',
            '"One Body Too Many","Archive","-1","Unknown","0001-01-01","Torrent"\n',
        ]
        for line in expected:
            assert line in result

    def test_search_anime(self, run):
        # GIVEN a search term
        # WHEN searching for it with --anime flag
        result = run("search", "-f", "csv", "ubuntu", "--anime", "--newest", "--limit", "3")[0]

        # THEN the results should only come from anime trackers
        expected = [
            '"ID","Name","Tracker","Seeds","Size","Uploaded","Available as"\n',
            '"ubuntustudio-12.04-dvd-amd64.iso","TokyoTosho","0","1.92GB","2012-07-14","Magnet link, Torrent"\n',
            '"ubuntu-13.04-desktop-i386.iso","TokyoTosho","0","794MB","2013-04-25","Magnet link, Torrent"\n',
            '"ubuntu-13.04-server-amd64.iso","TokyoTosho","0","701MB","2013-04-25","Magnet link, Torrent"\n',
        ]
        for line in expected:
            assert line in result

    def test_search_filter_legal(self, run):
        # GIVEN a search term
        # WHEN searching for it with --filter legal flag
        result = run(
            "search", "-f", "csv", "one body too many", "--filter", "legal", "--limit", "3"
        )[0]

        # THEN the results should only come from legal trackers
        expected = [
            '"ID","Name","Tracker","Seeds","Size","Uploaded","Available as"\n',
            '"One Body Too Many","Archive","-1","Unknown","0001-01-01","Torrent"\n',
        ]
        for line in expected:
            assert line in result

    def test_search_filter_anime(self, run):
        # GIVEN a search term
        # WHEN searching for it with --filter anime flag
        result = run(
            "search", "-f", "csv", "ubuntu", "--filter", "anime", "--newest", "--limit", "3"
        )[0]

        # THEN the results should only come from anime trackers
        expected = [
            '"ID","Name","Tracker","Seeds","Size","Uploaded","Available as"\n',
            '"ubuntustudio-12.04-dvd-amd64.iso","TokyoTosho","0","1.92GB","2012-07-14","Magnet link, Torrent"\n',
            '"ubuntu-13.04-desktop-i386.iso","TokyoTosho","0","794MB","2013-04-25","Magnet link, Torrent"\n',
            '"ubuntu-13.04-server-amd64.iso","TokyoTosho","0","701MB","2013-04-25","Magnet link, Torrent"\n',
        ]
        for line in expected:
            assert line in result
