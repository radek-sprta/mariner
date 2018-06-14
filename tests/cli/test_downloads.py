import pytest


@pytest.mark.usefixtures('results')
class TestDownloads:

    @pytest.mark.parametrize('tid, expected', [
        ('0', '"\x1b[35mName\x1b[0m","\x1b[35mSaved to\x1b[0m"\n"\x1b[33mubuntu-13.04-desktop-i386.iso\x1b[0m"'),
        ('1', '"\x1b[35mName\x1b[0m","\x1b[35mSaved to\x1b[0m"\n"\x1b[33mubuntu-13.04-server-amd64.iso\x1b[0m"'),
        ('2', '"\x1b[35mName\x1b[0m","\x1b[35mSaved to\x1b[0m"\n"\x1b[33mubuntustudio-12.04-dvd-amd64.iso\x1b[0m"')
    ],
        ids=['0', '1', '2'])
    def test_download(self, results, tid, expected, run):
        # GIVEN a list of results
        # WHEN trying to download them
        result = run('download', '-f', 'csv', tid)[0]

        # THEN it should download them and show information about it
        assert expected in result
