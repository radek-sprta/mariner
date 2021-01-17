"""Generla parse functions for Mariner."""


def number(unparsed_number: str) -> int:
    """Parse a number string from HTML page and return an integer.

    Args:
        unparsed_number: Number string to parse.

    Return:
        Parsed number.
    """
    if unparsed_number == "-":
        return 0
    squashed = unparsed_number.replace(" ", "")
    return int(squashed.replace(",", ""))


def date(unparsed_date: str) -> str:
    """Parse exotic date formats that Maya can't handle.

    Args:
        unparsed_date: Date string to parse.

    Return:
        Parsed date.
    """
    if unparsed_date.casefold() == "y-day":
        parsed_date = "yesterday"
    else:
        parsed_date = unparsed_date
    return parsed_date
