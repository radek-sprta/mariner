import subprocess

import pytest


@pytest.fixture
def run():
    def run_program(*args):
        args = ['mariner'] + list(args)
        result = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    return run_program


@pytest.fixture
def results(run):
    run('search', '-f', 'csv', '-t', 'tokyotosho', 'ubuntu', '--newest')
