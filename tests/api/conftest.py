import pytest
import cachalot

from mariner import searchengine


@pytest.fixture(scope='session')
def engine(tmpdir_factory):
    results_file = str(tmpdir_factory.mktemp(
        'search_results').join('results.json'))
    engine = searchengine.SearchEngine()
    engine.results = cachalot.Cache(path=results_file, size=1000)
    return engine


@pytest.fixture(scope='session')
def title():
    return 'Ubuntu'
