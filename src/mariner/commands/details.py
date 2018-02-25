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

    def take_action(self, parsed_args):
        """Show details for chosen torrent.

        Args:
            parsed_args: List of parsed arguments.

        Returns:
            List of details about chosen torrent.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)

        # Dictionary of attributes, that are not empty
        details = {d[0].strip('_').title(): d[1]
                   for d in torrent_.colored().__dict__.items() if d[1] is not None}
        ordered_details = self._order_details(details)

        colored_keys = (utils.magenta(key) for key in ordered_details)
        return (colored_keys, ordered_details.values())
