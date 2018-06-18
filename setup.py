#!/usr/bin/env python3
import os
import sys

import setuptools
from setuptools.command.test import test as TestCommand


requires = [
    'aiodns',
    'aiofiles',
    'aiohttp',
    'bs4',
    'cachalot >= 0.1.3',
    'cliff',
    'colorama',
    'future-fstrings',
    'lxml',
    'maya >= 0.3.4',
    'ruamel.yaml',
]

tests_require = [
    'pytest',
    'pytest-asyncio',
    'pytest-vcr',
    'vcrpy',
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
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


# Load package information from __version__.py
about = {}
with open(os.path.join(here, 'src', 'mariner', '__version__.py')) as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = '\n' + f.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    download_url=about['__download_url__'],
    license=about['__license__'],
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'mariner': ['config/*.yaml']},
    include_package_data=True,
    install_requires=requires,
    tests_require=tests_require,
    python_requires='>=3.5',
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': ['mariner = mariner.main:main'],
        'mariner.cli': [
            'config = mariner.commands.config:Config',
            'details = mariner.commands.details:Details',
            'download = mariner.commands.download:Download',
            'magnet = mariner.commands.magnet:Magnet',
            'open = mariner.commands.open:Open',
            'search = mariner.commands.search:Search',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
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
