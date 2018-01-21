# -*- coding: future_fstrings -*-
"""Contain CLI commands."""
import logging
import pathlib

from cliff import command, lister
import pyperclip

from mariner import downloader, torrent


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
        return parser

    def take_action(self, parsed_args):
        """Download chosen torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of downloaded torrents and the location where they were saved.
        """
        torrents = []
        for tid in parsed_args.ID:
            torrent_ = self.app.engine.result(tid)
            self.log.debug('tid=%s torrent=%s', tid, torrent_)
            if torrent_.torrent:
                torrents.append(torrent_)
                self.log.debug('Torrent appended.')
                self.log.info(f'Downloading torrent ID {tid}.')
            else:
                self.log.warning(
                    f'No torrent for {torrent_.name}. Use magnet link instead.')

        filelist = ((t.torrent, t.filename) for t in torrents)
        path = self.app.config['download_path']
        self.log.debug('filelist=%s download_path=%s', filelist, path)
        torrent_downloader = downloader.Downloader(download_path=path)
        torrent_downloader.download(filelist)

        headers = ('Name', 'Saved to')
        columns = ((t.name[:60], pathlib.Path(path) / t.filename)
                   for t in torrents)
        return (headers, columns)


class Magnet(command.Command):
    """Copy magnet link with given ID to clipboard."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Add arguments to argument parser.

        Args:
            prog_name: Application name.

        Returns:
            Instance of argument parser.
        """
        parser = super(Magnet, self).get_parser(prog_name)
        parser.add_argument(
            'ID', nargs=1, help='ID of the magnet link to copy', type=int)
        return parser

    def take_action(self, parsed_args):
        """Copy chosen magnet link to clipboard.

        Args:
            parsed_args: List of parsed arguments.
        """
        tid = parsed_args.ID[0]
        torrent_ = self.app.engine.result(tid)
        self.log.debug('tid=%s torrent=%s', tid, torrent)
        try:
            pyperclip.copy(torrent_.magnet)
            self.log.info(f'Copied {torrent_.name} magnet link to clipboard.')
            self.log.debug('magnet=%s', torrent_.magnet)
        except AttributeError:
            self.log.warning(
                f'{torrent_.name} has no magnet link. Download the torrent.')


class Search(lister.Lister):
    """Search for torrents."""

    log = logging.getLogger(__name__)

    @staticmethod
    def _availability(torrent_: torrent.Torrent) -> str:
        """Show whether it is available as torrent, magnet link or both."""
        availability = []
        if torrent_.magnet:
            availability.append('Magnet link')
        if torrent_.torrent:
            availability.append('Torrent')
        return ', '.join(availability)

    def get_parser(self, prog_name):
        """Add arguments to argument parser.

        Args:
            prog_name: Application name.

        Returns:
            Instance of argument parser.
        """
        parser = super().get_parser(prog_name)
        parser.add_argument('title', help='Title to search for')
        parser.add_argument('--limit', '-l', nargs='?', default=50,
                            help='Limit the number of results shown. Default is 50.',
                            type=int)
        plugins = self.app.engine.plugins.keys()
        parser.add_argument('--trackers', '-t', action='append', choices=plugins,
                            help='Trackers that should be searched', default=[])
        return parser

    def take_action(self, parsed_args):
        """Search for a torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of torrents found.
        """
        title = parsed_args.title
        limit = parsed_args.limit

        # If default tracker is used as default argument, the user provided ones
        # are appended to it, instead of replacing it.
        if not parsed_args.trackers:
            parsed_args.trackers.append(self.app.config['default_tracker'])
        trackers = [t.lower() for t in set(parsed_args.trackers)]

        self.log.info(f'Searching for "{title}".')
        self.log.debug('title=%s limit=%s trackers=%s', title, limit, trackers)
        results = self.app.engine.search(title, trackers, limit)

        headers = ('ID', 'Name', 'Tracker', 'Seeds', 'Available as')
        columns = ((tid, t.name[:80], t.tracker, t.seeds, self._availability(t))
                   for tid, t in results)
        return (headers, columns)
