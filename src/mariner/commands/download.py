# -*- coding: future_fstrings -*-
"""Mariner download command."""
import logging

from cliff import lister

from mariner import downloader, utils


class Download(lister.Lister):
    """Download torrent with given ID."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Add arguments to argument parser.

        Args:
            prog_name: Application name.

        Returns:
            Instance of argument parser.
        """
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'ID', nargs='+', help="ID of the torrent to download", type=int)
        parser.add_argument('--path', '-p', nargs='?',
                            help="Path to downloads torrent files to",
                            default=self.app.config['download_path'])
        return parser

    def take_action(self, parsed_args):
        """Download chosen torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of downloaded torrents and the location where they were saved.
        """
        path = parsed_args.path
        torrents = []
        for tid in parsed_args.ID:
            torrent_ = self.app.engine.result(tid)
            self.log.debug('tid=%s torrent=%s', tid, torrent_)
            if torrent_.torrent:
                torrents.append(torrent_)
                self.log.debug('Torrent appended.')
                self.log.info(f'Downloading torrent ID {utils.cyan(tid)}.')
            else:
                self.log.warning(utils.yellow(
                    f'No torrent for {torrent_.name}. Use magnet link instead.'))

        download_list = ((t.torrent, t.filename) for t in torrents)
        self.log.debug('download_list=%s download_path=%s',
                       download_list, path)
        torrent_downloader = downloader.Downloader(download_path=path)
        filelist = torrent_downloader.download(download_list)

        headers = ('Name', 'Saved to')
        colored_headers = [utils.magenta(h) for h in headers]
        columns = zip((t.colored().name for t in torrents), filelist)
        return (colored_headers, columns)
