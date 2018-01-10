import aiohttp
import pathlib
import pytest

from .context import mariner
from mariner import downloader


class TestDownloader:
    """Test the download manager."""
    @pytest.fixture
    def tmp_downloader(self, tmpdir):
        tmp = tmpdir.mkdir('test')
        return downloader.Downloader(tmp)

    @pytest.fixture
    def files(self):
        files = []
        files.append(('http://httpbin.org/image/png', 'png'))
        files.append(('http://httpbin.org/image/jpeg', 'jpeg'))
        files.append(('http://httpbin.org/image/webp', 'webp'))
        return files

    def test_download_coroutine(self, tmp_downloader, files, event_loop):
        session = aiohttp.ClientSession(loop=event_loop)
        url, name = files[0]
        event_loop.run_until_complete(
            tmp_downloader.download_coroutine(session, url, name))
        assert pathlib.Path(tmp_downloader.download_path, name).is_file()

    def test_download_filelist(self, tmp_downloader, files, event_loop):
        event_loop.run_until_complete(
            tmp_downloader.download_filelist(event_loop, files))
        for __, name in files:
            assert pathlib.Path(tmp_downloader.download_path, name).is_file()

    def test_download(self, tmp_downloader, files):
        tmp_downloader.download(files)
        for __, name in files:
            assert pathlib.Path(tmp_downloader.download_path, name).is_file()
