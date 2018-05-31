import pytest

from mariner import exceptions


class TestExceptions:
    """Test exception existance."""

    def test_base_error(self):
        """Error exists."""
        exception = exceptions.Error()
        assert exception
        assert Exception in exception.__class__.__bases__

    def test_no_result_exception(self):
        """NoResultException exists."""
        exception = exceptions.NoResultException()
        assert exception
        assert exceptions.Error in exception.__class__.__bases__

    def test_configuration_error(self):
        """ConfigurationError exists."""
        exception = exceptions.ConfigurationError()
        assert exception

    def test_input_error(self):
        """InputError exists."""
        exception = exceptions.InputError()
        assert exception
