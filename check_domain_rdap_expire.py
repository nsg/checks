#!/usr/bin/env python3

#
# A simple check that looks up domain expire information via the RDAP API
#

import sys
import os
import argparse
import json
from dateutil.parser import parse
from datetime import datetime, timezone
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", type=str, help="Look up the specified domain", required=True)
parser.add_argument("-p", "--provider", type=str, choices=["ascio"], help="RDAP Provider", required=True)
parser.add_argument("-w", "--warning", type=int, help="Warning level (days)", default=14)
parser.add_argument("-c", "--critical", type=int, help="Critical level (days)", default=7)
parser.add_argument("-C", "--cache_time", type=int, help="Cache time in seconds", default=21600)
args = parser.parse_args()

# https://lookup.icann.org/en/lookup
# https://deployment.rdap.org/
PROVIDERS = {
    "ascio": "https://rdap.ascio.com/domain/{domain}"
}

cache_file = f"/tmp/domain_expire_cache_{args.domain}.json"

if os.path.isfile(cache_file) and datetime.now().timestamp() < os.stat(cache_file).st_mtime + args.cache_time:
    cf = open(cache_file, "r")
    rdap_data = json.load(cf)
    rdap_data["cache"] = True
else:
    url = PROVIDERS[args.provider].format(domain=args.domain)
    resp = requests.get(url)

    if resp.status_code != 200:
        print("Got a non-200 responce from the RDAP provider")
        print("Response:", resp.text)
        sys.exit(3)

    rdap_data = json.loads(resp.text)
    cf = open(cache_file, "w")
    cf.write(json.dumps(rdap_data))
    rdap_data["cache"] = False

for event in rdap_data.get("events", []):
    if event.get("eventAction") == "expiration":
        expiration_date = parse(event.get("eventDate"))
        time_between = expiration_date - datetime.now(timezone.utc)
        print(f"Domain {args.domain} will expire in {time_between.days} days [cache: {rdap_data['cache']}]")

        if time_between.days < args.warning:
            sys.exit(1)
        elif time_between.days < args.critical:
            sys.exit(2)
        else:
            sys.exit(0)
