import pytest

from .context import mariner
from mariner import searchengine


class TestSearchEngineManager:
    """Test SearchEngineManager methods."""

    def test_find_plugins(self):
        pass

    def test_register_plugins(self):
        pass


class TestExceptions:
    """Test exception existance."""

    def test_base_error(self):
        """Error exists."""
        exception = searchengine.Error()
        assert exception
        assert Exception in exception.__class__.__bases__

    def test_no_result_exception(self):
        """NoResultException exists."""
        exception = searchengine.NoResultException()
        assert exception
        assert searchengine.Error in exception.__class__.__bases__
