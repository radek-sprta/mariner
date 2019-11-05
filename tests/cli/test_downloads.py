import pytest


@pytest.mark.usefixtures("results")
class TestDownloads:
    @pytest.mark.parametrize(
        "tid, expected",
        [
            (
                "0",
                '"Name","Saved to"\n"ubuntu-13.04-desktop-i386.iso"',
            ),
            (
                "1",
                '"Name","Saved to"\n"ubuntu-13.04-server-amd64.iso"',
            ),
            (
                "2",
                '"Name","Saved to"\n"ubuntustudio-12.04-dvd-amd64.iso"',
            ),
        ],
        ids=["0", "1", "2"],
    )
    def test_download(self, results, tid, expected, run):
        # GIVEN a list of results
        # WHEN trying to download them
        result = run("download", "-f", "csv", tid)[0]

        # THEN it should download them and show information about it
        assert expected in result
