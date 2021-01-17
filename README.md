# Mariner [![PyPI version](https://badge.fury.io/py/mariner.svg)](https://badge.fury.io/py/mariner) [![Pipeline status](https://gitlab.com/radek-sprta/mariner/badges/master/pipeline.svg)](https://gitlab.com/radek-sprta/mariner/commits/master) [![Coverage report](https://gitlab.com/radek-sprta/mariner/badges/master/coverage.svg)](https://gitlab.com/radek-sprta/mariner/commits/master) [![Downloads](http://pepy.tech/badge/mariner)](http://pepy.tech/project/mariner) [![Black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

Navigate torrents in CLI with Mariner. It offers a simple interface for streamlined experience. No more annoying ads and pop-up windows.

It is currently under heavy development, so expect breaking changes. Currently only works in Linux, but any contributions in this regard are welcome.

## Features

- Runs on Linux and Windows.
- Automatically get a working proxy for trackers that have them.
- Download torrent files and copy magnet links to clipboard.
- Open torrents in your default torrent application.
- Show torrent details.
- Asynchronous I/O for better responsiveness.
- Supports the following trackers:
  - Archive.org
  - Distrowatch
  - Etree
  - LimeTorrents
  - Linuxtracker
  - Nyaa
  - NyaaPantsu
  - TokyoTosho

![Mariner demonstration](docs/assets/mariner.svg)

## Installation

Mariner requires Python 3.6 or newer to run.

### Python package

You can easily install Mariner using pip. This is the preferred method:

`pip3 install mariner`

### Manual

Alternatively, to get the latest development version, you can clone this repository and then manually install it:

```bash
git clone git@gitlab.com:radek-sprta/mariner.git
cd mariner
poetry build
pip install dist/*.whl
```

## Usage

Mariner supports both interactive and non-interactive modes. To see the list of commands, simply type:

`mariner help`

In order to start Mariner in interactive mode, run it without any arguments:

`mariner`

Then search for Ubuntu torrents:

`(mariner) search Ubuntu -t linuxtracker`

and download the first result on the list:

`(mariner) download 0`

Alternatively, copy the magnet link to clipboard:

`(mariner) magnet 0`

Or open it in your torrent application:

`(mariner) open 0`

And quit the program:

`(mariner) quit`

For more information, check the [documentation].

## Contributing

For information on how to contribute to the project, please check the [Contributor's Guide][contributing]

## Disclaimer

I do not encourage anyone to act in conflict with their local laws and I do not endorse any illegal activity. Some content in the search results provided be Mariner might be illegal in your country and it is up to you to check your local laws before using it. Neither I, nor Mariner can be held liable for any action taken against you as the result of using it.

## Contact

[mail@radeksprta.eu](mailto:mail@radeksprta.eu)

[incoming+radek-sprta/mariner@gitlab.com](incoming+radek-sprta/mariner@gitlab.com)

## Acknowledgements

Mariner uses many excellent open-source libraries. But I would particularly like to mention the following, as without them, Mariner might not have been possible:

- [Aiohttp](https://github.com/aio-libs/aiohttp)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Cliff](https://github.com/openstack/cliff/tree/master/cliff)
- [TinyDB](https://github.com/msiemens/tinydb)

## License

GNU General Public License v3.0

[contributing]: https://gitlab.com/radek-sprta/mariner/blob/master/CONTRIBUTING.md
[documentation]: https://radek-sprta.gitlab.io/mariner
