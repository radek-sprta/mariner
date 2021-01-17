"""Color functions for Mariner."""
from typing import Any

import colorama


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
