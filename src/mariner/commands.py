# -*- coding: future_fstrings -*-
"""Contain CLI commands."""
import logging
import pathlib
import pprint
import subprocess

from cliff import command, lister, show
import pyperclip

from mariner import downloader, torrent


class ConfigCommand(command.Command):
    """Show or update configuration."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Add arguments to argument parser.

        Args:
            prog_name: Application name.

        Returns:
            Instance of argument parser.
        """
        parser = super().get_parser(prog_name)
        parser.add_argument('--show', '-s', action='store_true',
                            help='Show the configuration')
        parser.add_argument('key', nargs='?', help='Option to change', default=None)
        parser.add_argument('value', nargs='?', help='New value', default=None)
        return parser

    @staticmethod
    def _update_dict(dict_, key, value):
        """Update option in dictionary to a new value.

        Args:
            dict_: Dictionary to update.
            key: Option to update.
            value: New value.
        """
        dict_[key] = value if key in dict_ else (
            ConfigCommand._update_dict(c, key, value) for c in dict_.values())

    def take_action(self, parsed_args):
        """Copy chosen magnet link to clipboard.

        Args:
            parsed_args: List of parsed arguments.
        """
        key = parsed_args.key
        value = parsed_args.value
        show_ = parsed_args.show
        if not show_ and not (key and value):
            raise ValueError('Provide key and value to update or use --show')
        if show_:
            self.log.info('Mariner configuration:')
            pprint.pprint(self.app.config._config)  # pylint: disable=protected-access
        else:
            self._update_dict(self.app.config, key, value)
            self.log.info(f'Updated {key} to {value}')


class DetailsCommand(show.ShowOne):
    """Show details about torrent with given ID."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Add arguments to argument parser.

        Args:
            prog_name: Application name.

        Returns:
            Instance of argument parser.
        """
        parser = super().get_parser(prog_name)
        parser.add_argument('ID', help="ID of the torrent to show", type=int)
        return parser

    @staticmethod
    def _order_details(unordered):
        """Order results, so that Name is first.

        Args:
            unordered: Unordered results.

        Returns:
            ordered: Ordered results.
        """
        ordered = {}
        ordered['Name'] = unordered.pop('Name')
        ordered.update(unordered)
        # Shorten magnet link
        try:
            ordered['Magnet'] = ordered['Magnet'][:80] + '...'
        except KeyError:
            pass
        return ordered

    def take_action(self, parsed_args):
        """Show details for chosen torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of details about chosen torrent.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)

        # List of only information, that is not empty
        details = {d[0].title(): d[1]
                   for d in torrent_.__dict__.items() if d[1] is not None}
        details = self._order_details(details)

        return (details.keys(), details.values())


class DownloadCommand(lister.Lister):
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


class MagnetCommand(command.Command):
    """Copy magnet link with given ID to clipboard."""

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
            'ID', help='ID of the magnet link to copy', type=int)
        return parser

    def take_action(self, parsed_args):
        """Copy chosen magnet link to clipboard.

        Args:
            parsed_args: List of parsed arguments.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)
        self.log.debug('tid=%s torrent=%s', tid, torrent)
        try:
            pyperclip.copy(torrent_.magnet)
            self.log.info(f'Copied {torrent_.name} magnet link to clipboard.')
            self.log.debug('magnet=%s', torrent_.magnet)
        except AttributeError:
            self.log.warning(
                f'{torrent_.name} has no magnet link. Download the torrent.')


class OpenCommand(command.Command):
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

    def take_action(self, parsed_args):
        """Open chosen torrent in the default torrent application.

        Args:
            parsed_args: List of parsed arguments.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)
        self.log.debug('tid=%s torrent=%s', tid, torrent)
        try:
            self.log.info(f'Opening {torrent_.name} magnet link.')
            subprocess.call(['xdg-open', torrent_.magnet])
        except TypeError:
            self.log.info(f'Opening {torrent_.name}.')
            torrent_downloader = downloader.Downloader()
            torrent_downloader.download(
                [(torrent_.torrent, torrent_.filename)])
            torrent_file = torrent_downloader.download_path / torrent_.filename
            subprocess.call(['xdg-open', torrent_file])
            torrent_file.unlink()


class SearchCommand(lister.Lister):
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
        parser.add_argument('--limit', '-l', nargs='?',
                            default=self.app.config['results'],
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

        headers = ('ID', 'Name', 'Tracker', 'Seeds', 'Size', 'Available as')
        columns = ((tid, t.name[:80], t.tracker, t.seeds, t.size, self._availability(t))
                   for tid, t in results)
        return (headers, columns)
