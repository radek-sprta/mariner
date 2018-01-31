"""Define exceptions used within the Mariner module."""


class Error(Exception):
    """Base - class for all exceptions raised by this module."""


class NoResultException(Error):
    """No result found for given search string."""


class ConfigurationError(Error):
    """Illegal option in Configuration."""


class InputError(Error):
    """Wrong input by user."""
