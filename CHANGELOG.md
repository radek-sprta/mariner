# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Make timeout configurable.
- Support for Etree.org tracker.
- Support for Archive.org tracker.
- Search trackers with legal content only using --legal/-L option.
- Use uvloop when available.

### Fixed
- Update Distrowatch parser.
- Fix plugins sometimes not getting loaded.
- Fix config command.

## [1.1.0] - 2018-05-16
### Added
- Support for Nyaa.si tracker.
- Support for Limetorrents tracker.
- Set download path for downloading torrent files.
- Automatically get working proxy for ThePirateBay, LimeTorrents.

### Fixed
- Fix support for KickAssTorrents.
- Use cached results immediately, not after second search.

## [1.0.3] - 2018-03-04
### Fixed
- Add missing future_fstring coding to config command.

## [1.0.2] - 2018-03-04
### Fixed
- Fix path problems in Python 3.5.

## [1.0.1] - 2018-02-28
### Fixed
- Restore compatibility with Python 3.5.

## [1.0.0] - 2018-02-25
### Added
- Sort results by upload date using --newest/-n flag.
- Search all available trackers using --all/-a option.
- Colored output.
- Docker image.
- Support snaps.

### Changed
- Switch default tracker to Linuxtracker.

## [0.4.0] - 2018-02-01
### Added
- Open torrents in the default torrent application.
- Configure Mariner from within the application using config command.

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
[0.4.0]: https://gitlab.com/radek-sprta/mariner/compare/v0.3.0...v0.4.0
[1.0.0]: https://gitlab.com/radek-sprta/mariner/compare/v0.4.0...v1.0.0
[1.0.1]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.0...v1.0.1
[1.0.2]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.1...v1.0.2
[1.0.3]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.2...v1.0.3
[1.1.0]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.3...v1.1.0
