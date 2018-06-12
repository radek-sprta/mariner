import aiohttp
import pathlib
import pytest

from mariner import downloader


@pytest.fixture(scope='module')
def files():
    files = [('http://httpbin.org/image/png', 'png'),
             ('http://httpbin.org/image/jpeg', 'jpeg'),
             ('http://httpbin.org/image/webp', 'webp')]
    return files


class TestDownloader:
    """Test the download manager."""
    @pytest.fixture
    def tmp_downloader(self, tmpdir):
        tmp = str(tmpdir.mkdir('test'))
        return downloader.Downloader(tmp)

    @pytest.mark.parametrize('url, name', files())
    def test_download_coroutine(self, tmp_downloader, url, name, event_loop):
        # GIVEN a session
        session = aiohttp.ClientSession(loop=event_loop)
        # WHEN downloading a file
        downloaded = event_loop.run_until_complete(
            tmp_downloader.download_coroutine(session, url, name))
        # THEN it should be saved to the download path
        assert pathlib.Path(tmp_downloader.download_path, downloaded).is_file()

    @pytest.mark.smoke
    def test_download(self, tmp_downloader, files):
        # GIVEN a list of files
        # WHEN downloading the files
        downloaded = tmp_downloader.download(files)
        # THEN all of them should be downloaded
        count = 0
        for filename in downloaded:
            assert pathlib.Path(
                tmp_downloader.download_path, filename).is_file()
            count += 1
        assert count == 3
