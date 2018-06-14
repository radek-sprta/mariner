import pytest


@pytest.mark.usefixtures('results')
class TestDetails:

    @pytest.mark.xfail(reason='Sometimes fails on Python 3.5, requires more investigation')
    @pytest.mark.parametrize('tid,expected',
                             [
                                 (0, '\x1b[33mubuntu-13.04-desktop-i386.iso\x1b[0m\nTokyoTosho\nhttp://releases.ubuntu.com/13.04/ubuntu-13.04-desktop-i386.iso.torrent\nmagnet:?xt=urn:btih:3KWHACHC4OTOIMQZKDATC2IKZIQMLIEK&tr=http%3A%2F%2Ftorrent.ubu...\n794MB\n\x1b[32m0\x1b[0m\n\x1b[31m0\x1b[0m\n2013-04-25\n'),
                                 (1, '\x1b[33mubuntu-13.04-server-amd64.iso\x1b[0m\nTokyoTosho\nhttp://releases.ubuntu.com/13.04/ubuntu-13.04-server-amd64.iso.torrent\nmagnet:?xt=urn:btih:4UBTDIFIJGOZL34OXVKGCE6NAIJHLSDX&tr=http%3A%2F%2Ftorrent.ubu...\n701MB\n\x1b[32m0\x1b[0m\n\x1b[31m0\x1b[0m\n2013-04-25\n'),
                                 (2, '\x1b[33mubuntustudio-12.04-dvd-amd64.iso\x1b[0m\nTokyoTosho\nhttp://cdimage.ubuntu.com/ubuntustudio/releases/12.04/release/ubuntustudio-12.04-dvd-amd64.iso.torrent\nmagnet:?xt=urn:btih:C2XTZE5IIQTKTIKMZHXBVKALTT26PDZX&tr=http%3A%2F%2Ftorrent.ubu...\n1.92GB\n\x1b[32m0\x1b[0m\n\x1b[31m0\x1b[0m\n2012-07-14\n')
                             ],
                             ids=['0', '1', '2'])
    def test_show_details(self, tid, expected, run):
        # GIVEN search results
        # WHEN showing the details
        result = run('details', '-f', 'value', str(tid))[0]

        # THEN it should correctly display torrent details
        assert result == expected

    def test_show_details_no_result(self, run):
        # GIVEN search results
        # WHEN showing the details of non-existing result
        result = run('details', '-f', 'value', '100')[1]

        # THEN it should show error with the passed ID
        expected = 'No torrent with ID 100\n'
        assert result == expected
