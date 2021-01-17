"""Mariner magnet command."""
import logging

from cliff import command
import pyperclip

from mariner.utils import color


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
        parser = super().get_parser(prog_name)
        parser.add_argument("ID", help="ID of the magnet link to copy", type=int)
        return parser

    def take_action(self, parsed_args):
        """Copy chosen magnet link to clipboard.

        Args:
            parsed_args: List of parsed arguments.
        """
        tid = parsed_args.ID
        torrent_ = self.app.engine.result(tid)
        self.log.debug("tid=%s torrent=%s", tid, torrent_)
        try:
            pyperclip.copy(torrent_.magnet)
            self.log.info(f"Copied {torrent_.colored().name} magnet link to clipboard.")
            self.log.debug("magnet=%s", torrent_.magnet)
        except pyperclip.PyperclipException:
            pyperclip.copy(torrent_.torrent)
            self.log.warning(color.yellow(f"{torrent_.name} has no magnet link."))
            self.log.info(f"Copied {torrent_.colored().name} torrent URL to clipboard instead.")
