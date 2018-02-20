"""CLI config command."""
import logging
import pprint

from cliff import command

from mariner import utils


class Config(command.Command):
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
            Config._update_dict(c, key, value) for c in dict_.values())

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
