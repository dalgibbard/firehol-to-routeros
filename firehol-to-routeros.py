#!/bin/env python3
import requests
import argparse
import ipaddress

default_url = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
default_dest_file = 'firehol.rsc'


def checkip(cidr):
    try:
        return str(ipaddress.ip_network(cidr))
    except ValueError as err:
        raise ValueError(f'Unexpected value from Source URL: {err}')


parser = argparse.ArgumentParser(
    description='Small python script to produce RouterOS compatible blocklists from FireHOL Level1',
)
parser.add_argument('-u', help="Source URL for Firehol List (just a list of IP CIDRs)", dest="source_url")
parser.add_argument('-o', help='Output file to create', dest="dest_file")
inputargs = parser.parse_args()
source_url = inputargs.source_url or default_url
dest_file = inputargs.dest_file or default_dest_file

r = requests.get(source_url)
if not r.status_code == 200:
    print(f"Error fetching FireHOL list from {source_url} - error: {r.status_code} - body: {r.text}")
    exit(1)
ip_list = [cidr.decode() for cidr in r.content.splitlines() if not cidr.decode().startswith('#') and checkip(cidr.decode())]
if not ip_list:
    print("Fetched list was empty!")
    exit(1)
# Overwrites any existing files
with open(dest_file, 'w') as f:
    f.write("/ip firewall address-list\n")
    [f.write(f" add list=firehol comment=firehol address={cidr}\n") for cidr in ip_list]

print(f"Successfully created ouput file: {dest_file}")
