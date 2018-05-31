# -*- coding: future_fstrings -*-
"""Mariner search command."""
import logging

from cliff import lister

from mariner import torrent, utils


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
        parser.add_argument('--all', '-a', action='store_true',
                            help='Search all available trackers')
        parser.add_argument('--legal', '-L', action='store_true',
                            help='Search trackers with legal content only')
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

    def _parse_trackers(self, parsed_args):
        """Return a list of trackers to use.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of trackers to use.
        """

        if parsed_args.all:
            # Use all trackers
            trackers = self.app.engine.plugins.keys()
        elif parsed_args.legal:
            # Use only legal trackers
            trackers = [t for t in self.app.engine.plugins.keys(
            ) if self.app.engine.plugins[t].legal]
        else:
            # If default tracker is used as default argument, the user provided ones
            # are appended to it, instead of replacing it.
            if not parsed_args.trackers:
                parsed_args.trackers.append(self.app.config['default_tracker'])
            trackers = [t.lower() for t in set(parsed_args.trackers)]
        return trackers

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

        trackers = self._parse_trackers(parsed_args)

        self.log.info(f'Searching for {utils.cyan(title)}.')
        self.log.debug('title=%s limit=%s trackers=%s',
                       title, limit, trackers)
        results = self.app.engine.search(
            title, trackers, limit, sort_by_newest=newest)

        headers = ('ID', 'Name', 'Tracker', 'Seeds',
                   'Size', 'Uploaded', 'Available as')
        # Headers cannot be a generator, as it messes up alignment
        colored_headers = [utils.magenta(h) for h in headers]
        colored_results = ((tid, t.colored()) for tid, t in results)
        columns = ((tid,
                    t.name,
                    t.tracker,
                    t.seeds,
                    t.size,
                    t.date,
                    self._availability(t))
                   for tid, t in colored_results)
        return (colored_headers, columns)
