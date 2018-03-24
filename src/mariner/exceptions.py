"""Define exceptions used within the Mariner module."""


class Error(Exception):
    """Base - class for all exceptions raised by this module."""


class ConfigurationError(Error):
    """Illegal option in Configuration."""


class InputError(Error):
    """Wrong input by user."""


class NoProxyAvailable(Error):
    """No proxy available for given tracker."""


class NoResultException(Error):
    """No result found for given search string."""


class PluginError(Error):
    """Error in one of the plugins."""
