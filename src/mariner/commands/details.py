"""Mariner details command."""
import logging

from cliff import show

from mariner import utils


class Details(show.ShowOne):
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
