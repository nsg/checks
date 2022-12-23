#!/bin/bash

DOMAIN="$2"
CACHE_STATE_DIR="/tmp/domain_expire_cache_$DOMAIN"

query_whois() {
  find $CACHE_STATE_DIR -mmin +360 -delete
  if [ ! -e "$CACHE_STATE_DIR" ]; then
    whois "$DOMAIN" > $CACHE_STATE_DIR
  fi
}

w() {
  cat "$CACHE_STATE_DIR"
}

str_to_age() {
  local now="$( date +%s )"
  local ts="$( date -d "$1" +%s )"
  local ago="$(( now - ts ))"
  echo "$(( ago / 86400 ))"
}

query_whois

if w | grep -q "The Swedish Internet Foundation"; then
  CREATED="$(w | awk '/^created/{ print $2 }')"
  MODIFIED="$(w | awk '/^modified/{ print $2 }')"
  EXPIRES="$(w | awk '/^expires/{ print $2 }')"
elif w | grep -q "whois.ascio.com"; then
  CREATED="$(w | awk '/^   Creation Date/{ print $3 }')"
  MODIFIED="$(w | awk '/^   Updated Date/{ print $3 }')"
  EXPIRES="$(w | awk '/^   Registry Expiry Date/{ print $4 }')"
elif w | grep -q "whois.namecheap.com"; then
  CREATED="$(w | awk '/^   Creation Date/{ print $3 }')"
  MODIFIED="$(w | awk '/^   Updated Date/{ print $3 }')"
  EXPIRES="$(w | awk '/^   Registry Expiry Date/{ print $4 }')"
else
  echo "Unknown WHOIS data format"
  exit 3
fi

NOW_TS="$( date +%s )"

EXPIRES_TS="$( date -d "$EXPIRES" +%s )"
EXPIRES_IN="$(( EXPIRES_TS - NOW_TS ))"
EXPIRES_IN_DAYS="$(( EXPIRES_IN / 86400 ))"

echo -n "Expires $EXPIRES (mod: $MODIFIED; create: $CREATED)"
echo -n "|expire_in_days=$EXPIRES_IN_DAYS;14;7;0;365"
echo -n " modified_ago=$(str_to_age $MODIFIED);"
echo -n " created_ago=$(str_to_age $CREATED);"
echo

if [[ $EXPIRES_IN_DAYS -lt 14 ]]; then
  exit 1
elif [[ $EXPIRES_IN_DAYS -lt 30 ]]; then
  exit 2
fi

exit 0
