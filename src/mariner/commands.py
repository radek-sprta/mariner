# -*- coding: future_fstrings -*-
"""Contain CLI commands."""
import logging
import pathlib

from cliff import command, lister
import pyperclip

from mariner import downloader, searchengine
from mariner.plugins import distrowatch


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
        parser.add_argument('ID', nargs='+', type=int)
        return parser

    def take_action(self, parsed_args):
        """Download chosen torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of downloaded torrents and the location where they were saved.
        """
        engine = distrowatch.Distrowatch()

        torrents = []
        for tid in parsed_args.ID:
            torrent = engine.get_torrent(tid)
            self.log.debug('tid=%s torrent=%s', tid, torrent)
            if torrent.torrent_url:
                torrents.append(torrent)
                self.log.debug('Torrent appended.')
                self.log.info(f'Downloading torrent ID {tid}.')
            else:
                self.log.warning(
                    f'No torrent for {torrent.name}. Use magnet link instead.')

        filelist = ((t.torrent_url, t.filename) for t in torrents)
        path = self.app.config['download_path']
        self.log.debug('filelist=%s download_path=%s', filelist, path)
        torrent_downloader = downloader.Downloader(download_path=path)
        torrent_downloader.download(filelist)

        headers = ('ID', 'Name', 'Saved to')
        columns = ((t.tid, t.name[:60], pathlib.Path(path) / t.filename)
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
        parser.add_argument('ID', nargs=1, type=int)
        return parser

    def take_action(self, parsed_args):
        """Copy chosen magnet link to clipboard.

        Args:
            parsed_args: List of parsed arguments.
        """
        engine = distrowatch.Distrowatch()
        tid = parsed_args.ID[0]
        torrent = engine.get_torrent(tid)
        self.log.debug('tid=%s torrent=%s', tid, torrent)
        if torrent.magnet_link:
            pyperclip.copy(torrent.magnet_link)
            self.log.info(f'Copied {torrent.name} magnet link to clipboard.')
            self.log.debug('magnet=%s', torrent.magnet_link)
        else:
            self.log.warning(
                f'{torrent.name} has no magnet link. Download the torrent.')


class Search(lister.Lister):
    """Search for torrents."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Add arguments to argument parser.

        Args:
            prog_name: Application name.

        Returns:
            Instance of argument parser.
        """
        parser = super().get_parser(prog_name)
        parser.add_argument('title', nargs=1)
        parser.add_argument('--limit', '-l', nargs='?', default=10, type=int)
        parser.add_argument('--tracker', '-t', nargs='?',
                            default=self.app.config['default_tracker'])
        return parser

    def take_action(self, parsed_args):
        """Search for a torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of torrents found.
        """
        title = parsed_args.title[0].lower()
        limit = parsed_args.limit
        tracker = parsed_args.tracker.lower()
        self.log.debug('title=%s limit=%s tracker=%s', title, limit, tracker)

        self.log.info(f'Searching for "{title}".')
        engine = searchengine.engines[tracker]()
        torrents = engine.search(title, limit)
        self.log.debug(f'torrents={torrents}')

        headers = ('ID', 'Name', 'Available as')
        columns = ((t.tid, t.name[:80], t.mods) for t in torrents)
        return (headers, columns)
