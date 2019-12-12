# -*- coding: future_fstrings -*-
"""Generla parse functions for Mariner."""


def number(number: str) -> int:
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


def date(date: str) -> str:
    """Parse exotic date formats that Maya can't handle.

    Args:
        date: Date string to parse.

    Return:
        Parsed date.
    """
    if date.casefold() == 'y-day':
        return 'yesterday'
    return date
