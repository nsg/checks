#!/usr/bin/env python3

#
# A simple check that uses the loopia API to figure out when domains expire
# Create an API user, select advanced permissions and grant getDomain.
#

import os
import sys
import argparse
from datetime import datetime
from dateutil.parser import parse
import json
import xmlrpc.client

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", type=str, help="Look up the specified domain", required=True)
parser.add_argument("-u", "--user", type=str, help="Loopia API username", required=True)
parser.add_argument("-p", "--password", type=str, help="Loopia API password", required=True)
parser.add_argument("-w", "--warning", type=int, help="Warning level (days)", default=30)
parser.add_argument("-c", "--critical", type=int, help="Critical level (days)", default=14)
parser.add_argument("-C", "--cache_time", type=int, help="Cache time in seconds", default=21600)
args = parser.parse_args()

def get_domain_info():
    cache_file = f"/tmp/loopia_domain_expire_cache_{args.domain}.json"
    now_ts = datetime.now().timestamp()

    if os.path.isfile(cache_file) and now_ts < os.stat(cache_file).st_mtime + args.cache_time:
        cf = open(cache_file, "r")
        data = json.load(cf)
        data["cache"] = int((os.stat(cache_file).st_mtime + args.cache_time - now_ts) / 60)
        return data

    client = xmlrpc.client.ServerProxy(uri="https://api.loopia.se/RPCSERV", encoding="utf-8")
    response = client.getDomain(args.user, args.password, args.domain)
    cf = open(cache_file, "w")
    cf.write(json.dumps(response))
    response["cache"] = 0
    return response

response = get_domain_info()
paid = response['paid']
expiration_date = parse(response['expiration_date'])
time_between = expiration_date - datetime.now()

if paid:
    print(f"Domain {args.domain} will expire in {time_between.days} days [cache: {response['cache']}]")
else:
    print(f"Domain {args.domain} is not paid, it will expire in {time_between.days} days [cache: {response['cache']}]")

if time_between.days < args.warning:
    sys.exit(2)
elif time_between.days < args.critical:
    sys.exit(1)
elif not paid:
    sys.exit(2)
else:
    sys.exit(0)
