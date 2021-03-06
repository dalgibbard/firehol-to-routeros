# firehol-to-routeros
Small python script to produce RouterOS compatible blocklists from FireHOL Level1

Also configurable enough to take any URL containing a list of CIDRs and make a custom RouterOS compatible Address-List

## Setup
It's assumed that you'd use this script to produce a RouterOS-compatible Firehol blocklist,
and then host this from a webserver somewhere.

### Run the Script to generate firehole.rsc
```text
$ python3 firehol-to-routeros.py
```

Optionally, define your own output file or source URL; see the help output for info:
```text
$ python3 firehol-to-routeros.py -h
usage: firehol-to-routeros.py [-h] [-u SOURCE_URL] [-o DEST_FILE]

Small python script to produce RouterOS compatible blocklists from FireHOL Level1

optional arguments:
  -h, --help     show this help message and exit
  -u SOURCE_URL  Source URL for Firehol List (just a list of IP CIDRs)
  -o DEST_FILE   Output file to create
```

* Copy the created ```firehol.rsc``` file to a webserver etc.

## Setup RouterOS
Then setup RouterOS as follows (be sure to change naming if you're using this for something other than Firehol :) ):

```text
# Create A Downloader Script
/system/script/add name="downloadfirehol" \
    dont-require-permissions=yes \
    source={/tool fetch url="https://my-hosted-script-domain.com/firehol.rsc" \
    mode=https \
    output=file \
    dst-path=firehol.rsc;}

# Create an Updater Script
/system/script/add name="replacefirehol" \
    policy=read,write \
    dont-require-permissions=no \
    source={/file
       :global firehol [/file get firehol.rsc contents];
       :if (firehol != "") do={/ip firewall address-list remove [find where comment="firehol"]
       /import file-name=firehol.rsc;}}

# Setup a Downloader Schedule
/system/scheduler/add start-time=06:00:00 interval=6h name=downloadfirehol on-event=downloadfirehol

# Setup an Updater Schedule
/system/scheduler/add start-time=06:05:00 interval=6h name=replacefirehol on-event=replacefirehol
```
