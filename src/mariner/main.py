"""Entrance point for Mariner application."""
import os
import pathlib
import sys
from typing import List

from cliff import app, commandmanager

from mariner import __version__
from mariner import searchengine, utils, config


class Mariner(app.App):
    """Interactive CLI for Mariner."""

    def __init__(self):
        super().__init__(
            description=__version__.__description__,
            version=__version__.__version__,
            command_manager=commandmanager.CommandManager('mariner.cli'),
            deferred_help=True,
        )
        self.config = config.Config().load()

    def build_option_parser(self, description, version, argparse_kwargs=None):
        """Return an Argparse option parser for Mariner.

        Args:
            description: Mariner description.
            version: Mariner version.
        """
        # Override the help message for log output
        kwargs = {'conflict_handler': 'resolve'}
        parser = super().build_option_parser(description, version, kwargs)
        parser.add_argument(
            '--log-file',
            action='store',
            default=None,
            help='Specify a file to log output. Default ~/.local/share/mariner/mariner.log.',
        )
        return parser

    def configure_logging(self):
        """Create logging handlers for any log output."""
        # Set logging to file by default.
        if not self.options.log_file:
            log_dir = os.getenv('XDG_DATA_HOME', '~/.local/share/mariner')
            log_dir = utils.check_path(log_dir)
            self.options.log_file = pathlib.Path(log_dir) / 'mariner.log'
        super().configure_logging()

    def initialize_app(self, argv: List[str]) -> None:
        """Initialize the application.

        Args:
          argv: List[str]: List of command line arguments.
        """
        self.LOG.debug('Initialize Mariner')
        # Initialize plugins
        searchengine.SearchEngineManager().initialize_engines()

    def prepare_to_run_command(self, cmd) -> None:
        """Code to run before command.

        Args:
          cmd: Command to run.
        """
        self.LOG.debug('Preparing to run command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err) -> None:
        """Code to run after command.

        Args:
          cmd: Command that was run.
          result: Result of the command.
          err: Errors caught while running the command.
        """
        self.LOG.debug('Clean up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('Got an error: %s', err)


def main(argv=sys.argv[1:]):  # pylint: disable=dangerous-default-value
    """Application entrance point.

    Args:
      argv: Defaults to sys.argv[1:]. Command line argument list.
    """
    mariner = Mariner()
    return mariner.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
