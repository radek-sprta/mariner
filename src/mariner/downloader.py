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

    async def download_coroutine(self, session: Session, url: Url, name: str) -> None:
        """Download a single file and asynchronously save it to disk.

        Args:
            url: URL of file.
            name: Name of file.
        """
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                filename = self.download_path / name
                self.log.debug('filename=%s', filename)
                async with aiofiles.open(filename, 'wb') as file_:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            self.log.debug('saved=%s', filename)
                            break
                        await file_.write(chunk)

    async def download_filelist(self, loop: Loop, filelist: List[File]) -> None:
        """Download all files in the list asychronously.

        Args:
            loop: AsyncIO loop.
            filelist: List of files to download.
        """
        async with aiohttp.ClientSession(loop=loop) as session:
            for url, name in filelist:
                self.log.debug('Downloading url=%s name=%s', url, name)
                await self.download_coroutine(session, url, name)

    def download(self, filelist: List[File]) -> None:
        """Run a loop to download all files in the list.

        Args:
            filelist: List of files to download.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download_filelist(loop, filelist))
