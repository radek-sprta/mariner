# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2019-10-20

### Added

- New --anime/-A flag to search only on anime trackers.
- New --filter/-F flag to search on trackers with certain tags. Enables general filters on trackers.
- Support for Anidex.info tracker.
- Support for Nyaa.pantsu.cat tracker.
- Extend plugins framework to enable other request types than get.
- Support for Python 3.8.

### Changed

- Lower cache validity to 4 hours.
- With torrents that have no magnet link, magnet command copies torrent URL instead.

### Fixed

- Quote URL when opening torrent, so it cannot be interpreted as shell command.
- Fix KickAssTorrents tracker.
- Correctly interpret '-' as number of seeds/leeches.
- Translate Y-day to yesterday, so it's parsed correctly.

## [1.3.1] - 2019-01-25

### Added

- Install correct Cachalot version.

## [1.3.0] - 2019-01-14

### Added

- Define path to configuration file using --config-file option.
- Open multiple torrents at once with the open command.
- Support for Python 3.7.
- Alises for Limetorrents (lime) and TokyoTosho (tt).

### Changed

- Change user agent to Firefox 62 to avoid blocking.
- Proxy plugins use a fallback, if they cannot get an online proxy.
- Improved download command display.

### Fixed

- Fix getting results from multipage PirateBay results.
- No Nyaa results should have None for title anymore.
- Distrowatch, Limetorrents and TPB should no longer throw error when returning no results.
- Fix Etree search.
- Fix Linuxtracker plugin.
- Save results in $HOME/.cache/mariner directory.

### Removed

- Remove Docker image.
- Remove Snap, as right now Snapcraft crashes when building Mariner.
- Remove LimeTorrents proxies, as they blocked Mariner using Cloudflare.

## [1.2.0] - 2018-06-20

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
- Strip whitespace from KickAssTorrents sizes.
- Fix sorting by newest when some torrents don't have date.

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
[1.2.0]: https://gitlab.com/radek-sprta/mariner/compare/v1.1.0...v1.2.0
[1.3.0]: https://gitlab.com/radek-sprta/mariner/compare/v1.2.0...v1.3.0
[1.3.1]: https://gitlab.com/radek-sprta/mariner/compare/v1.3.0...v1.3.1
[1.4.0]: https://gitlab.com/radek-sprta/mariner/compare/v1.3.1...v1.4.0
