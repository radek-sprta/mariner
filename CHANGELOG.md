# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Open torrents in default torrent application
- Configuration Mariner from within the application

## [0.3.0] - 2018-01-28
### Added
- Configure default number of results shown.
- New 'details' command, that shows additional information about torrent.
- Display torrent size in the search results.

### Changed
- Refactor cache into separate Cachalot package.

## [0.2.0] - 2018-01-21
### Added
- Search on multiple trackers at once.
- Search on Linuxtracker and KickAssTorrents.
- Add aliases for PirateBay and KickAssTorrents.
- Write help messages for arguments.

### Changed
- Order results by number of seeds.
- Rotate logs after 1 MB.

## [0.1.1] - 2018-01-10
### Added
- Support for Python 3.5 using future-fstrings.

## 0.1 - 2018-01-10
### Added
- Command line interface to search Distrowatch, PirateBay and Tokyotosho.
- Ability to download torrent files and copy magnet links to clipboard.
- Online documentation available at [https://radek-sprta.gitlab.io/mariner](https://radek-sprta.gitlab.io/mariner).

[0.1.1]: https://gitlab.com/radek-sprta/mariner/compare/v0.1.0...v0.1.1
[0.2.0]: https://gitlab.com/radek-sprta/mariner/compare/v0.1.1...v0.2.0
[0.3.0]: https://gitlab.com/radek-sprta/mariner/compare/v0.2.0...v0.3.0
