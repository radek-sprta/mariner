"""Download a list of files to given location."""
import asyncio
import logging
import pathlib
from typing import List, Tuple, Union, Generator

import aiofiles
import aiohttp
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from mariner import utils

Url = str
Path = Union[str, pathlib.Path]
File = Tuple[Url, str]


class Downloader:
    """Handle file downloads asynchronously."""

    log = logging.getLogger(__name__)

    def __init__(self, download_path: Path = '~/Downloads', timeout: int = 10) -> None:
        self.download_path = utils.check_path(download_path)
        self.timeout = timeout

    async def download_coroutine(self,
                                 session: aiohttp.ClientSession,
                                 url: Url,
                                 name: str) -> Path:
        """Download a single file and asynchronously save it to disk.

        Args:
            url: URL of file.
            name: Name of file.

        Returns:
            Path of downloaded file.
        """
        filename = self.download_path / name
        self.log.debug('filename=%s', filename)
        async with session.get(url, timeout=self.timeout) as response:
            # Cast filename to str as workaround for Python 3.5
            async with aiofiles.open(str(filename), 'wb') as file_:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        self.log.debug('saved=%s', filename)
                        break
                    await file_.write(chunk)
        return filename

    async def _download_all(self, download_list: List[File]) -> Generator:
        """Run a loop to download all files in the list.

        Args:
            download_list: List of files to download.

        Return:
            List of downloaded files.
        """
        async with aiohttp.ClientSession() as session:
            tasks = asyncio.as_completed([self.download_coroutine(
                session, url, name) for url, name in download_list])
            return await asyncio.gather(*tasks)

    def download(self, download_list: List[File]) -> Generator:
        """Run a loop to download all files in the list.

        Args:
            download_list: List of files to download.

        Return:
            List of downloaded files.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._download_all(download_list))
