# firehol-to-routeros
Small python script to produce RouterOS compatible blocklists from FireHOL Level1

## Setup
It's assumed that you'd use this script to produce a RouterOS-compatible Firehol blocklist,
and then host this from a webserver somewhere.

### Run the Script to generate firehole.rsc
```bash
python3 firehol-to-routeros.py
```

* Copy the created ```firehol.rsc``` file to a webserver etc.

## Setup RouterOS
Then setup RouterOS as follows:

```text
# Create A Downloader Script
/system/script/add name="downloadfirehol" \
    dont-require-permissions=yes
    source=/tool fetch url="https://my-hosted-script-domain.com/firehol.rsc" \
    mode=https \
    output=file \
    dst-path=firehol.rsc;

# Create an Updater Script
/system/script/add name="replacefirehol" \
    policy=read,write \
    dont-require-permissions=no \
    source=/file
       :global firehol [/file get firehol.rsc contents];
       :if (firehol != "") do={/ip firewall address-list remove [find where comment="firehol"]
       /import file-name=firehol.rsc;}

# Setup a Downloader Schedule
/system/scheduler/add start-time=06:00:00 interval=6h name=downloadfirehol on-event=downloadfirehol

# Setup an Updater Schedule
/system/scheduler/add start-time=06:05:00 interval=6h name=replacefirehol on-event=downloadfirehol
```
