"""Download a list of files to given location."""
import asyncio
import logging
import pathlib
from typing import List, Tuple, Union

import aiofiles
import aiohttp
import async_timeout

from mariner import utils

Url = str
Path = Union[str, pathlib.Path]
File = Tuple[Url, str]
Loop = asyncio.selector_events.BaseSelectorEventLoop
Session = aiohttp.ClientSession


class Downloader:
    """Handle file downloads asynchronously."""

    log = logging.getLogger(__name__)

    def __init__(self, download_path: Path = '~/Downloads') -> None:
        self.download_path = utils.check_path(download_path)

    async def download_coroutine(self, session: Session, url: Url, name: str) -> Path:
        """Download a single file and asynchronously save it to disk.

        Args:
            url: URL of file.
            name: Name of file.

        Returns:
            Path of downloaded file.
        """
        filename = self.download_path / name
        self.log.debug('filename=%s', filename)
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                async with aiofiles.open(filename, 'wb') as file_:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            self.log.debug('saved=%s', filename)
                            break
                        await file_.write(chunk)
        return filename

    async def download_filelist(self, loop: Loop, download_list: List[File]) -> List[Path]:
        """Download all files in the list asychronously.

        Args:
            loop: AsyncIO loop.
            filelist: List of files to download.

        Returns:
            List of downloaded files.
        """
        filelist = []
        async with aiohttp.ClientSession(loop=loop) as session:
            for url, name in download_list:
                self.log.debug('Downloading url=%s name=%s', url, name)
                filelist.append(await self.download_coroutine(session, url, name))
        return filelist

    def download(self, download_list: List[File]) -> List[Path]:
        """Run a loop to download all files in the list.

        Args:
            download_list: List of files to download.

        Return:
            List of downloaded files.
        """
        loop = asyncio.get_event_loop()
        filelist = loop.run_until_complete(self.download_filelist(loop, download_list))
        return filelist
