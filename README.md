![PyPI package version][pypi]

# Mariner

Mariner is a command line torrent searcher. It offers a simple interface for streamlined experience. No more annoying ads and pop-up windows.

It is currently under heavy development, so expect breaking changes. Currently only works in Linux, but any contributions in this regard are welcome.

## Features

- Search for torrents on Distrowatch, PirateBay and TokyoTosho.
- Download torrent files and copy magnet links to clipboard.
- Asynchronous I/O for better responsiveness.

## Installation

Mariner requires Python 3.6 to run.

**Python package**

Since it is written in pure Python, you can easily install it using pip:

`pip3 install mariner`

**Manual**

Alternatively, to get the latest development version, you can clone this repository and then manually install Mariner:

```
git clone git@gitlab.com:radek-sprta/mariner.git
cd mariner
python3 setup.py install
```

## Usage

Mariner supports both interactive and non-interactive modes. To see the list of commands, simply type:

`mariner help`

In order to start Mariner in interactive mode, run it without any arguments:

`mariner`

Then search for Ubuntu torrents:

`(mariner) search Ubuntu`

and download the first result on the list:

`(mariner) download 0`

Alternatively, copy the magnet link to clipboard:

`(mariner) magnet 0`

And quit:

`(mariner) quit`

For more information, check the [documentation][documentation].

## TODO
- Add more trackers for searching
- Allow searching multiple torrent trackers at once
- Show torrent details
- Pass torrents directly to Transmission and Deluge

## Contributing
For information on how to contribute to the project, please check the [Contributor's Guide][contributing]

## Disclaimer
I do not want anyone to act in conflict with their local laws and I do not endorse any illegal activity. Some content in the search results provided be Mariner might be illegal in your country and it is up to you to check your local laws before using it. Neither I, nor Mariner can be held liable for any action taken against you as the result of using it.

## Contact
[mail@radeksprta.eu](mailto:mail@radeksprta.eu)

## License
GNU General Public License v3.0

[contributing]: https://gitlab.com/radek-sprta/mariner/blob/master/CONTRIBUTING.md
[documentation]: https://radek-sprta.gitlab.io/mariner
[pypi]: https://badge.fury.oi/py/mariner.png
