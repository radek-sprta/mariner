# -*- coding: future_fstrings -*-
"""Utility functions for Mariner."""
import pathlib
from typing import Any, Union

import colorama


def check_path(path: Union[str, pathlib.Path]) -> pathlib.Path:
    """Check if path exists. If not, create it.

    Args:
      path: Path to check.

    Returns:
      Resulting path.
    """
    # Convert to Path object if needed
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    path = path.expanduser()

    # If path points to a file, get the parent directory
    directory = path.parent if path.suffix else path

    # Create path if needed
    directory.mkdir(parents=True, exist_ok=True)

    return path


def color(string: Any, text_color: str) -> str:
    """Color string in given color.

    Arguments:
        string: String to color.
        color: Defaults to yellow. Color to use.

    Returns:
        Colored string.
    """
    colors = {}
    colors['blue'] = colorama.Fore.BLUE
    colors['cyan'] = colorama.Fore.CYAN
    colors['green'] = colorama.Fore.GREEN
    colors['magenta'] = colorama.Fore.MAGENTA
    colors['red'] = colorama.Fore.RED
    colors['yellow'] = colorama.Fore.YELLOW
    if text_color not in colors.keys():
        raise ValueError(f'{text_color} is not a supported color.')
    return ''.join([colors[text_color], str(string), colorama.Style.RESET_ALL])


def cyan(string: Any) -> str:
    """Color string cyan."""
    return color(string, 'cyan')


def green(string: Any) -> str:
    """Color string cyan."""
    return color(string, 'green')


def magenta(string: Any) -> str:
    """Color string magenta."""
    return color(string, 'magenta')


def red(string: Any) -> str:
    """Color string red."""
    return color(string, 'red')


def yellow(string: Any) -> str:
    """Color string yellow."""
    return color(string, 'yellow')
