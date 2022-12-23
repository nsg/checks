# ✅ Nagios/Icinga Checks

This repository contains various active check scripts that I use from my Icinga server to monitor various things in my life.

## ⏰ Domain name expire checking

A bunch of scripts that monitors domain expire dates. It's really annoying to forget to renew a domain. I did this once and... never again!

### domain_expire.sh

Use the WHOIS protocol. Not the best looking script, quick and dirty script that does the job for me. TODO: rewrite this in python.

The WHOIS data is quite unstructured so it's possible that I do not support the format that your provider outputs.

### check_domain_rdap_expire.py

I wrote this because a few domains do not publish expire information in the whois data, but I'm able to look up the data via the newer RDAP protocol.

At the moment I only support ascio, but it's easy to add more providers.

```
usage: check_domain_rdap_expire.py [-h] -d DOMAIN -p {ascio} [-w WARNING] [-c CRITICAL] [-C CACHE_TIME]

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Look up the specified domain
  -p {ascio}, --provider {ascio}
                        RDAP Provider
  -w WARNING, --warning WARNING
                        Warning level (days)
  -c CRITICAL, --critical CRITICAL
                        Critical level (days)
  -C CACHE_TIME, --cache_time CACHE_TIME
                        Cache time in seconds
```

### check_domain_loopia_expire.py

I have a few domains where the expire date it hidden, this check will use the DNS registrar Loopias API to pull the domains expire data.

```
usage: check_domain_loopia_expire.py [-h] -d DOMAIN -u USER -p PASSWORD [-w WARNING] [-c CRITICAL]
                                     [-C CACHE_TIME]

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Look up the specified domain
  -u USER, --user USER  Loopia API username
  -p PASSWORD, --password PASSWORD
                        Loopia API password
  -w WARNING, --warning WARNING
                        Warning level (days)
  -c CRITICAL, --critical CRITICAL
                        Critical level (days)
  -C CACHE_TIME, --cache_time CACHE_TIME
                        Cache time in seconds
```
