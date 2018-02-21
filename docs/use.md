# Usage
Mariner has command line interface with the following commands:
- help
- search
- config
- details
- download
- magnet
- open

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

To search all available trackers, use `--all` or `-a` flag:

`mariner search -a OpenSuse`

By default, top 60 results are shown. To change that, use the `--limit` or `-l` flag:

`mariner search -l 20 OpenSuse`

To order the results by their upload date, you can use the `--newest` or `-n` flag:

`mariner search OpenSuse -n`

## Config
You can configure Mariner to better suit your needs with the `config` command. To list the current configuration, run it with the `--show` or `-s` flag:

`mariner config --show`

The command takes two positional arguments, to adjust the settings - key and value:

`mariner config default_tracker linuxtracker`

## Details
Shows the details of chosen torrent, such as upload date and number of seeds and leeches. Give it torrent ID as argument:

`mariner details 10`

## Download
Downloads torrents with given IDs to the download folder (default: ~/Downloads). You can download multiple torrent files at once:

`mariner download 1 2 3`

## Magnet
The Magnet command copies the magnet link of the torrent with given ID to clipboard.

`mariner magnet 5`

## Open
Open the torrent in your default torrent application.

`mariner open 5`

## Interactive mode
Mariner also supports interactive mode. Start it by running mariner without any arguments:

`mariner`

After that, you will see the `(mariner)` prompt. In interactive mode, you can run multiple commands in succession and take advantage of command history. When done, use Ctrl+D or the quit command to exit:

`(mariner) quit`
