# -*- coding: future_fstrings -*-
"""Contain CLI commands."""
import logging
import os
import pathlib
import pprint
import subprocess

from cliff import command, lister, show
import pyperclip

from mariner import downloader, torrent, utils


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
        parser.add_argument(
            'key', nargs='?', help='Option to change', default=None)
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
            pprint.pprint(
                self.app.config._config)  # pylint: disable=protected-access
        else:
            self._update_dict(self.app.config, key, value)
            self.log.info(
                f'Updated {utils.green(key)} to {utils.green(value)}')


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

    @staticmethod
    def _color_details(details):
        """Color details.

        Args:
            unordered: Unordered results.

        Returns:
            colored: Ordered results.
        """
        try:
            details['Name'] = utils.yellow(details['Name'])
            details['Seeds'] = utils.green(details['Seeds'])
            details['Leeches'] = utils.red(details['Leeches'])
        except KeyError:
            pass
        return details

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
        details = {d[0].strip('_').title(): d[1]
                   for d in torrent_.__dict__.items() if d[1] is not None}
        colored_details = self._color_details(details)
        ordered_details = self._order_details(colored_details)

        colored_keys = (utils.magenta(key) for key in ordered_details)
        return (colored_keys, ordered_details.values())


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
                self.log.info(f'Downloading torrent ID {utils.cyan(tid)}.')
            else:
                self.log.warning(utils.yellow(
                    f'No torrent for {torrent_.name}. Use magnet link instead.'))

        filelist = ((t.torrent, t.filename) for t in torrents)
        path = self.app.config['download_path']
        self.log.debug('filelist=%s download_path=%s', filelist, path)
        torrent_downloader = downloader.Downloader(download_path=path)
        torrent_downloader.download(filelist)

        headers = ('Name', 'Saved to')
        colored_headers = (utils.magenta(h) for h in headers)

        columns = ((utils.yellow(t.name[:60]), pathlib.Path(path) / t.filename)
                   for t in torrents)
        return (colored_headers, columns)


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
            self.log.info(
                f'Copied {utils.green(torrent_.name)} magnet link to clipboard.')
            self.log.debug('magnet=%s', torrent_.magnet)
        except AttributeError:
            self.log.warning(utils.yellow(
                f'{torrent_.name} has no magnet link. Download the torrent.'))


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
            return torrent_downloader.download_path / torrent_.filename
        return torrent_.magnet

    def take_action(self, parsed_args):
        """Open chosen torrent in the default torrent application.

        Args:
            parsed_args: List of parsed arguments.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)
        self.log.debug('tid=%s torrent=%s', tid, torrent)
        self.log.info(f'Opening {utils.cyan(torrent_.name)}.')
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
        parser.add_argument('--all', '-a', action='store_true',
                            help='Search all available trackers')
        parser.add_argument('--limit', '-l', nargs='?',
                            default=self.app.config['results'],
                            help='Limit the number of results shown. Default is 50.',
                            type=int)
        parser.add_argument('--newest', '-n', action='store_true',
                            help='Sort results by newest')
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
        newest = parsed_args.newest

        if parsed_args.all:
            # Use all trackers
            trackers = self.app.engine.plugins.keys()
        else:
            # If default tracker is used as default argument, the user provided ones
            # are appended to it, instead of replacing it.
            if not parsed_args.trackers:
                parsed_args.trackers.append(self.app.config['default_tracker'])
            trackers = [t.lower() for t in set(parsed_args.trackers)]

        self.log.info(f'Searching for {utils.cyan(title)}.')
        self.log.debug('title=%s limit=%s trackers=%s', title, limit, trackers)
        results = self.app.engine.search(
            title, trackers, limit, sort_by_newest=newest)

        headers = ('ID', 'Name', 'Tracker', 'Seeds',
                   'Size', 'Uploaded', 'Available as')
        # Heads cannot be a generator, otherwise it messes up alignment
        colored_headers = [utils.magenta(h) for h in headers]
        columns = ((tid,
                    utils.yellow(t.name[:80]),
                    t.tracker,
                    utils.green(t.seeds),
                    t.size,
                    t.date,
                    self._availability(t))
                   for tid, t in results)
        return (colored_headers, columns)
