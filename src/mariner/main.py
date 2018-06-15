"""Entrance point for Mariner application."""
import logging
import os
import pathlib
import sys
from typing import List

from cliff import app, commandmanager
import colorama

from mariner import __version__
from mariner import searchengine, utils, config


class Mariner(app.App):
    """Interactive CLI for Mariner."""

    log = logging.getLogger(__name__)

    def __init__(self):
        super().__init__(
            description=__version__.__description__,
            version=__version__.__version__,
            command_manager=commandmanager.CommandManager('mariner.cli'),
            deferred_help=True,
        )
        self.config = config.Config()
        self.config.load()

        # Older configurations have no timeout option
        # Also, cast timeout to int, int case it was string
        try:
            timeout = int(self.config['timeout'])
        except KeyError:
            timeout = 10
            self.config['timeout'] = timeout

        self.engine = searchengine.SearchEngine(timeout=timeout)

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
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        # Set logging to file by default.
        if not self.options.log_file:
            log_dir = os.getenv('XDG_DATA_HOME', '~/.local/share/mariner')
            log_dir = utils.check_path(log_dir)
            self.options.log_file = str(pathlib.Path(log_dir) / 'mariner.log')

        # Monkey patched to use RotatingFileHandler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=self.options.log_file, maxBytes=1000000, backupCount=1)
        formatter = logging.Formatter(self.LOG_FILE_MESSAGE_FORMAT)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Always send higher-level messages to the console via stderr
        console = logging.StreamHandler(self.stderr)
        console_level = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
        }.get(self.options.verbose_level, logging.DEBUG)
        console.setLevel(console_level)
        formatter = logging.Formatter(self.CONSOLE_MESSAGE_FORMAT)
        console.setFormatter(formatter)
        root_logger.addHandler(console)

    def initialize_app(self, argv: List[str]) -> None:
        """Initialize the application.

        Args:
          argv: List[str]: List of command line arguments.
        """
        self.LOG.debug('Initialize Mariner')
        # Initialize color output
        colorama.init()
        if self.interactive_mode:
            self.log.info(
                'Welcome to Mariner, a command line torrent searcher!')
            self.log.info(
                'Type "help" or see http://radek-sprta.gitlab.io/mariner to get started.')

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
