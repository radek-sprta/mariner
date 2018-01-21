# Usage
Mariner has command line interface with the following commands:
- help
- search
- download
- magnet

You can run them by typing:

`mariner COMMAND ARGUMENTS`

Let's take a look at them one by one.

## Help
Help lists all of Mariner's commands and optional arguments. You can pass it a command as an argument, to see more information about it.

`mariner help help`

## Search
Searches a torrent tracker for torrents. It requires one positional argument - the search phrase:

`mariner search OpenSuse`

By default, it searches Distrowatch. You can use `--tracker` or `-t` flag to use Linuxtracker, or some other tracker instead:

`mariner search -t linuxtracker OpenSuse`

You can list all the available trackers via:

`mariner help search`

Some of them have aliases you can use in place of the full names, for example tpb for PirateBay or kat for KickAssTorrents:

`mariner search -t kat OpenSuse`

You can also search on multiple trackers at once. Just use multiple `-t` flags:

`mariner search -t distrowatch -t linuxtracker OpenSuse`

By default, top 60 results are shown. To change that, use the `--limit` or `-l` flag:

`mariner search -l 20 OpenSuse`

## Download
Downloads torrents with given IDs to the download folder (default: ~/Downloads). You can download multiple torrent files at once:

`mariner download 1 2 3`

## Magnet
The Magnet command copies the magnet link of the torrent with given ID to clipboard.

`mariner magnet 5`

## Interactive mode
Mariner also supports interactive mode. Start it by running mariner without any arguments:

`mariner`

After that, you will see the `(mariner)` prompt. In interactive mode, you can run multiple commands in succesion and take advantage of command history. When done, use Ctrl+D or the quit command to exit:

`(mariner) quit`
