# -*- coding: future_fstrings -*-
"""Mariner open command."""
import logging
import os
import subprocess  # nosec

from cliff import command

from mariner import downloader


class Open(command.Command):
    """Open torrent in the default torrent application."""

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
            'ID', help='ID of the torrent to open', type=int)
        return parser

    @staticmethod
    def _get_torrent_link(torrent_):
        """Get a link torrent, that can be opened by xdg-open.

        Args:
            torrent: Torrent object.

        Returns:
            Openable torrent link.
        """
        if torrent_.torrent:
            torrent_downloader = downloader.Downloader()
            torrent_downloader.download(
                [(torrent_.torrent, torrent_.filename)])
            return str(torrent_downloader.download_path / torrent_.filename)
        return torrent_.magnet

    def take_action(self, parsed_args):
        """Open chosen torrent in the default torrent application.

        Args:
            parsed_args: List of parsed arguments.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)
        self.log.debug('tid=%s torrent=%s', tid, torrent_)
        self.log.info(f'Opening {torrent_.colored().name}.')
        link = self._get_torrent_link(torrent_)
        if self.app.options.verbose_level > 1:
            subprocess.run(['xdg-open', link])
        else:
            with open(os.devnull) as devnull:
                subprocess.run(['xdg-open', link],
                               stdout=devnull, stderr=devnull)
        try:
            # Try deleting the file, if it exists
            link.unlink()
        except AttributeError:
            pass
