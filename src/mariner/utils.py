# -*- coding: future_fstrings -*-
"""Utility functions for Mariner."""
import os
import pathlib
import platform
import subprocess  # nosec
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


def cache_path() -> pathlib.Path:
    """Cache path for the application.

    Returns:
        Cache path for the application.
    """
    if platform.system() == "Linux":
        config_dir = os.getenv("XDG_CACHE_HOME", "~/.cache")
        cache_dir = ""
    elif platform.system() == "Windows":
        config_dir = os.getenv("APPDATA")
        cache_dir = "Cache"
    return pathlib.Path(config_dir, "mariner", cache_dir, "cache.json")


def config_path() -> pathlib.Path:
    """Configuration path for the application.

    Returns:
        Configuration path for the application.
    """
    if platform.system() == "Linux":
        config_dir = os.getenv("XDG_CONFIG_HOME", "~/.config")
    elif platform.system() == "Windows":
        config_dir = os.getenv("APPDATA")
    return pathlib.Path(config_dir, "mariner")


def data_path() -> pathlib.Path:
    """Data path for the application.

    Returns:
        Data path for the application.
    """
    if platform.system() == "Linux":
        data_dir = os.getenv("XDG_DATA_HOME", "~/.local/share")
    elif platform.system() == "Windows":
        data_dir = os.getenv("APPDATA")
    return pathlib.Path(data_dir, "mariner")


def download_path() -> pathlib.Path:
    """User's download path.

    Returns:
        User's download path.
    """
    return pathlib.Path("~/Downloads").expanduser()


def log_path() -> pathlib.Path:
    """Log path for the application.

    Returns:
        Log path for the application.
    """
    if platform.system() == "Linux":
        data_dir = os.getenv("XDG_DATA_HOME", "~/.local/share")
        log_dir = "log"
    elif platform.system() == "Windows":
        data_dir = os.getenv("APPDATA")
        log_dir = "Logs"
    return pathlib.Path(data_dir, "mariner", log_dir)


def color(string: Any, text_color: str) -> str:
    """Color string in given color.

    Arguments:
        string: String to color.
        color: Defaults to yellow. Color to use.

    Returns:
        Colored string.
    """
    colors = {}
    colors["blue"] = colorama.Fore.BLUE
    colors["cyan"] = colorama.Fore.CYAN
    colors["green"] = colorama.Fore.GREEN
    colors["red"] = colorama.Fore.RED
    colors["yellow"] = colorama.Fore.YELLOW
    if text_color not in colors.keys():
        raise ValueError(f"{text_color} is not a supported color.")
    return "".join([colors[text_color], str(string), colorama.Style.RESET_ALL])


def cyan(string: Any) -> str:
    """Color string cyan."""
    return color(string, "cyan")


def green(string: Any) -> str:
    """Color string cyan."""
    return color(string, "green")


def red(string: Any) -> str:
    """Color string red."""
    return color(string, "red")


def yellow(string: Any) -> str:
    """Color string yellow."""
    return color(string, "yellow")


def open_file(path: str, *, verbose=False) -> None:
    """Open file in OS's default application.

    Args:
        path: Path to the file.
        verbose: Print verbose output.
    """
    if platform.system() == "Linux":
        if verbose:
            subprocess.run(["xdg-open", path], check=False)
        else:
            with open(os.devnull) as devnull:
                subprocess.run(["xdg-open", path], stdout=devnull, stderr=devnull, check=False)
    elif platform.system() == "Windows":
        os.startfile(path)  # pylint: disable=no-member


def parse_number(number: str) -> int:
    """Parse a number string from HTML page and return an integer.

    Args:
        number: Number string to parse.

    Return:
        Parsed number.
    """
    if number == "-":
        return 0
    squashed = number.replace(" ", "")
    return int(squashed.replace(",", ""))


def parse_date(date: str) -> str:
    """Parse exotic date formats that Maya can't handle.

    Args:
        date: Date string to parse.

    Return:
        Parsed date.
    """
    if date.casefold() == 'y-day':
        return 'yesterday'
    return date
