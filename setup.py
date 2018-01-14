#!/usr/bin/env python3
import os
import pathlib
import sys

import setuptools
from setuptools.command.test import test as TestCommand


requires = [
    'aiodns',
    'aiofiles',
    'aiohttp',
    'bs4',
    'cliff',
    'future-fstrings',
    'jsonpickle',
    'lxml',
    'pendulum',
    'ruamel.yaml',
    'tinydb',
    'tinydb_smartcache',
]

tests_require = [
    'pytest',
    'pytest-asyncio',
]

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


about = {}
with pathlib.Path(here, 'src', 'mariner', '__version__.py').open() as f:
    exec(f.read(), about)
with open('README.md', 'r') as f:
    readme = '\n' + f.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    download_url=about['__download_url__'],
    license=about['__license__'],
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'mariner': ['config/*.yaml']},
    install_requires=requires,
    tests_require=tests_require,
    python_requires='>=3.5',
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': ['mariner = mariner.main:main'],
        'mariner.cli': [
            'download = mariner.commands:Download',
            'magnet = mariner.commands:Magnet',
            'search = mariner.commands:Search',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search", ] + [
        ('Programming Language :: Python :: %s' % x) for x in
        '3 3.5 3.6'.split()
    ],
    zip_safe=False,
)
